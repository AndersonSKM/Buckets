from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from accounts.models import User
from accounts.services import user_from_uuidb64
from accounts.utils import user_activation_token, validate_password

USER_FIELDS = (
    'uri',
    'pk',
    'email',
    'first_name',
    'last_name',
)

USER_READ_ONLY_FIELDS = (
    'is_superuser',
    'is_staff',
    'is_active',
    'last_login',
    'created_at',
    'updated_at',
)

CREATE_USER_FIELDS = USER_FIELDS + (
    'password',
    'password_confirm'
)


class UUIDAndTokenSerializerMixin(serializers.Serializer):
    uuidb64 = serializers.RegexField('[0-9A-Za-z_\-]+')
    token = serializers.RegexField('[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}')
    token_generator = default_token_generator

    default_error_messages = {
        'invalid_uuid': "Invalid user id or user doesn't exist.",
        'invalid_token': "Invalid token for given user.",
    }

    def validate_uuidb64(self, value):
        self.user = user_from_uuidb64(value)
        if not self.user:
            self.fail('invalid_uuid')
        return value

    def validate(self, data):
        data = super().validate(data)
        if not self.token_generator.check_token(self.user, data['token']):
            self.fail('invalid_token')
        return data


class PasswordValidationMixin(serializers.Serializer):
    def validate(self, data):
        data = super().validate(data)
        password = data.get('password')
        validate_password(password, user=self.user)
        return data


class PasswordConfirmSerializerMixin(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    default_error_messages = {
        'password_mismatch': "Passwords don't match.",
    }

    def validate(self, data):
        data = super().validate(data)
        password = data.get('password')
        password_confirm = data.pop('password_confirm')

        if password != password_confirm:
            self.fail('password_mismatch')
        return data


class UserSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='auth:users-detail')
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = USER_FIELDS + USER_READ_ONLY_FIELDS
        read_only_fields = USER_READ_ONLY_FIELDS


class UserCreateSerializer(UserSerializer, PasswordConfirmSerializerMixin):
    class Meta:
        model = User
        fields = CREATE_USER_FIELDS

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(email, password, False, **validated_data)
        validate_password(password, user)
        return user


class UserActivateSerializer(UUIDAndTokenSerializerMixin):
    token_generator = user_activation_token


class UserPasswordForgotSerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'invalid_email': "Invalid email or user doesn't exist.",
    }

    def validate_email(self, value):
        self.user = User.objects.get_active_or_none(email=value)
        if not self.user:
            self.fail('invalid_email')
        return value


class UserPasswordResetSerializer(UUIDAndTokenSerializerMixin, PasswordValidationMixin,
                                  PasswordConfirmSerializerMixin):
    pass


class UserChangePasswordSerializer(PasswordValidationMixin, PasswordConfirmSerializerMixin):
    current_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    default_error_messages = {
        'invalid_current_password': "Invalid current password.",
    }

    def validate_current_password(self, value):
        self.user = self.context['request'].user
        if not self.user.check_password(value):
            self.fail('invalid_current_password')
        return value
