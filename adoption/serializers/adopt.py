from rest_framework import serializers
from adoption.models.adopt import Adoption, PetAdoption
from pets.models.petInfo import Pet
from users.models.userInfo import UserProfile

class PetAdoptionSerializer(serializers.ModelSerializer):
    petId = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(), source='pet')
    dataAdocao = serializers.DateTimeField()

    class Meta:
        model = PetAdoption
        fields = ['petId', 'dataAdocao']

class GetAdoptionSerializer(serializers.ModelSerializer):
    clientId = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    pet_links = PetAdoptionSerializer(many=True, read_only=True)

    class Meta:
        model = Adoption
        fields = ['id', 'clientId', 'pet_links']

class AdoptionSerializer(serializers.Serializer):
    clientId = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    petId = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(), source='pet')
    