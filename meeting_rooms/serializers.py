from rest_framework import serializers
from .models import MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField()
    custom_name = serializers.CharField(required=False)
    capacity = serializers.IntegerField()

    class Meta:
        model = MeetingRoom
        fields = '__all__'
