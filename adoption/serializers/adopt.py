from rest_framework import serializers
from adoption.models.adopt import AllowAdoption

class AllowAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowAdoption
        fields = '__all__'
        read_only_fields = ['dataAdocao']
