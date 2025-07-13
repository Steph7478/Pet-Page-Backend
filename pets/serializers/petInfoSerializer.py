from rest_framework import serializers
from pets.models.petInfo import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['status']
