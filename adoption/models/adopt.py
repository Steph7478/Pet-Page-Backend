from django.db import models
from pets.models.petInfo import Pet
from users.models.userInfo import UserProfile

class Adoption(models.Model):
    class Meta:
        db_table = 'adoptions'

    clientId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    petId = models.ManyToManyField(Pet, through='PetAdoption')

class PetAdoption(models.Model):
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE, related_name='pet_links')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    dataAdocao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adoptions_petId'
