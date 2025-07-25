from django.db import models
import uuid
from users.models.userInfo import UserProfile

class Pet(models.Model):
    class Meta:
        db_table = 'pets'

    PET_STATUS = (
        ("pendente", "pendente"),
        ("disponivel", "disponivel"),
        ("adotado", "adotado")
    )
    PET_PORTE = (
        ("Pequeno", "Pequeno"),
        ("Médio", "Médio"),
        ("Grande", "Grande")
    )

    petId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ownerId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    nome = models.CharField(max_length=100)
    raca = models.CharField(max_length=100)
    porte = models.CharField(max_length=100, choices=PET_PORTE)
    idade = models.IntegerField()
    descricao = models.CharField(max_length=1000)
    localizacao = models.CharField(max_length=100)
    fotoUrl = models.URLField(max_length=1000)
    status = models.CharField(max_length=100, choices=PET_STATUS, default='disponivel')
