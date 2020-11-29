from rest_framework import serializers
from calculadora.models import Consecucion , Objetivo

class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = '__all__'

class ConsecucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consecucion
        fields = '__all__'