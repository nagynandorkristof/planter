from rest_framework import serializers
from .models import Plant


class PlantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    recommended_watering_interval = serializers.IntegerField()
    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_at = serializers.DateTimeField(read_only=True)

class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)

    
class WateringLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())
    watered_at = serializers.DateTimeField(read_only=True)
    watered_by = serializers.ReadOnlyField(source='watered_by.username')
    image = serializers.ImageField(required=False, allow_null=True)

    
class WateringSerializer(serializers.Serializer):
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.filter(archived=False))
    image = serializers.ImageField(required=False, allow_null=True)

    def validate_plant(self, value):
        if not Plant.objects.filter(id=value.id, archived=False).exists():
            raise serializers.ValidationError("Plant with this ID does not exist or is archived.")
        return value
    
class SubscriptionSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(source='user.username')
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.filter(archived=False))
    subscribed_at = serializers.DateTimeField(read_only=True)

    def validate_plant(self, value):
        if not Plant.objects.filter(id=value.id, archived=False).exists():
            raise serializers.ValidationError("Plant with this ID does not exist or is archived.")
        return value
