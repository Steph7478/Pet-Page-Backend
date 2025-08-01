from users.models.userInfo import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'role']

    def get_id(self, obj):
        try:
            return str(obj.profile.id)
        except UserProfile.DoesNotExist:
            return None

    def get_role(self, obj):
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return None
