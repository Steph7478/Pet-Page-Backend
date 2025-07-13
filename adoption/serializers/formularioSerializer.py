from rest_framework import serializers
from adoption.models.formulario import Formulario

class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = '__all__'
