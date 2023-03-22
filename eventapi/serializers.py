from rest_framework import serializers
from base.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'category', 'location', 'price', 'date_time', 'creator']