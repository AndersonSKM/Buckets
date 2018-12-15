from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from accounts.models import User
from accounts.utils import user_activation_token

USER_FIELDS = (
    'url',
    'pk',
    'email',
    'first_name',
    'last_name',
)

USER_READ_ONLY_FIELDS = (
    'is_active',
    'created_at',
    'updated_at',
)

CREATE_USER_FIELDS = USER_FIELDS + (
    'password',
    'password_confirm'
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='accounts:users-detail', read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = USER_FIELDS + USER_READ_ONLY_FIELDS
        read_only_fields = USER_READ_ONLY_FIELDS


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = CREATE_USER_FIELDS

    def create(self, validated_data):
        data = validated_data.copy()
        return User.objects.create_user(
            email=data.pop('email'),
            password=data.pop('password'),
            confirm=data.pop('password_confirm'),
            is_staff=False,
            **data
        )


class UUIDAndTokenSerializerMixin(serializers.Serializer):
    uuidb64 = serializers.RegexField('[0-9A-Za-z_\\-]+')
    token = serializers.RegexField('[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}')
    token_generator = default_token_generator

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        data['user'] = User.objects.get_user_by_uuid_token(
            uuidb64=attrs['uuidb64'],
            token=attrs['token'],
            generator=self.token_generator
        )
        return data


class UserActivateSerializer(UUIDAndTokenSerializerMixin):
    token_generator = user_activation_token


class UserPasswordResetSerializer(UUIDAndTokenSerializerMixin):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    token_generator = default_token_generator


class UserPasswordForgotSerializer(serializers.Serializer):
    email = serializers.EmailField()
    default_error_messages = {
        'invalid_email': "Invalid email or user doesn't exist.",
    }

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        data['user'] = User.objects.get_active_or_none(email=attrs['email'])
        if not data['user']:
            self.fail('invalid_email')
        return data


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
