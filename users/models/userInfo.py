import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuário"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE_CHOICES = (
        ('adotante', 'adotante'),
        ('anunciante', 'anunciante'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100, default='Usuário')
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'
