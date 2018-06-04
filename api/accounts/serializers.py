from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='api:users-detail')
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'uri',
            'pk',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            'created_at',
            'updated_at',
        )

    def create(self, data):
        data.pop('is_active', False)
        return get_user_model().objects.create_user(
            data.pop('email', None),
            data.pop('password', None),
            data.pop('is_staff', False),
            **data
        )

    def update(self, instance, data):
        instance.email = data.get('email', instance.email)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.is_staff = data.get('is_staff', instance.is_staff)
        instance.is_active = data.get('is_active', instance.is_active)
        instance.save()
        return instance
