from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'created_at', 'updated_at',)
        read_only_fields = ('id', 'email', 'created_at', 'updated_at',)
