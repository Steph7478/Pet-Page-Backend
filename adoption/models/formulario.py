from django.db import models
from users.models.userInfo import UserProfile
from pets.models.petInfo import Pet
from django.core.validators import EmailValidator

class Formulario(models.Model):
    class Meta:
        db_table = 'formulario'

    AMBIENTE_CHOICES = (
        ('Casa', 'Casa'),
        ('Apartamento', 'Apartamento'),
    )
    
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='formularios')
    clientId = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='formularios_enviados')
    email = models.CharField(
        max_length=254,
        validators=[EmailValidator()]
    )
    telefone = models.CharField(max_length=20)
    motivo = models.TextField()
    ambiente = models.CharField(max_length=50, choices=AMBIENTE_CHOICES)
    espacoExterno = models.BooleanField(default=True)
    teveAnimaisAntes = models.BooleanField(default=True)
    ambienteSeguro = models.BooleanField(default=True)

    def __str__(self):
        return f"Formulario para {self.petId} por {self.clientId}"
