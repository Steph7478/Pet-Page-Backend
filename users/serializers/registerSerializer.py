from rest_framework import serializers
from django.contrib.auth.models import User

from users.models.userInfo import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.is_active = True
        user.save()
        
        UserProfile.objects.create(user_id=user.id, role=role, name=user.username)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['role'] = instance.profile.role if hasattr(instance, 'profile') else None
        return rep
