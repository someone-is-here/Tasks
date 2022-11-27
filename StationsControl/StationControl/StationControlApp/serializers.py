from rest_framework import serializers

from StationControlApp.models import Station, Indication


class StationSerializer(serializers.ModelSerializer):
    """
    class for serializing station
    """
    class Meta:
        model = Station
        fields = "__all__"


class IndicationSerializer(serializers.ModelSerializer):
    """
    class for serializing indication
    """
    class Meta:
        model = Indication
        fields = ('axis', 'distance')
