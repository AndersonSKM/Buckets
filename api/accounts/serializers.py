from rest_framework import serializers

from accounts.models import User
from accounts.services import user_from_uuidb64
from accounts.utils import user_activation_token

USER_FIELDS = (
    'uri',
    'pk',
    'email',
    'first_name',
    'last_name',
    'is_superuser',
    'is_staff',
    'is_active',
    'last_login',
    'created_at',
    'updated_at',
)

CREATE_USER_FIELDS = USER_FIELDS + (
    'password',
    'password_confirm',
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='auth:users-detail')
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_superuser = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = USER_FIELDS


class FullUserSerializer(UserSerializer):
    is_staff = serializers.BooleanField(read_only=False)


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    default_error_messages = {
        'invalid_passwords': "Passwords don't match.",
    }

    class Meta:
        model = User
        fields = CREATE_USER_FIELDS

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            self.fail('invalid_passwords')
        return data

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        is_staff = validated_data.pop('is_staff', False)
        return User.objects.create_user(email, password, is_staff, **validated_data)


class FullUserCreateSerializer(UserCreateSerializer):
    is_staff = serializers.BooleanField(read_only=False)


class UserActivateSerializer(serializers.Serializer):
    uuidb64 = serializers.RegexField('[0-9A-Za-z_\-]+')
    token = serializers.RegexField('[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}')

    default_error_messages = {
        'invalid_uuid': "Invalid user id or user doesn\'t exist.",
        'invalid_token': "Invalid token for given user.",
    }

    def validate(self, data):
        data = super(UserActivateSerializer, self).validate(data)

        self.user = user_from_uuidb64(data['uuidb64'])
        if not self.user:
            self.fail('invalid_uuid')

        if not user_activation_token.check_token(self.user, data['token']):
            self.fail('invalid_token')
        return data
