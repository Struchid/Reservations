from rest_framework import serializers

from .models import MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField()
    custom_name = serializers.CharField(required=False)
    capacity = serializers.IntegerField()

    class Meta:
        model = MeetingRoom
        fields = '__all__'

    def validate(self, data):
        if data.get('capacity') == 0:
            message = 'Capacity of the room must be a positive integer'
            raise serializers.ValidationError(message)
        return data
