from rest_framework import serializers
from .models import Station, Equipment, Sensor, SensorData

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.nom', read_only=True)
    capteur_name = serializers.CharField(source='capteur.nom', read_only=True)

    class Meta:
        model = SensorData
        fields = ['id', 'valeur', 'timestamp', 'equipment', 'capteur', 'equipment_name', 'capteur_name']

