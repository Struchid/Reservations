from rest_framework import serializers

from .models import MeetingRoom, Reservation, User
from meeting_rooms.utils.error_codes import ErrorCodes as error_codes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'

    def validate(self, data):
        if data.get('capacity') <= 0:
            raise serializers.ValidationError(error_codes.CAPACITY_NOT_POSITIVE_INTEGER_ERROR)
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        meeting_room_id = data.get('meeting_room').id
        time_from = data.get('time_from')
        time_to = data.get('time_to')
        reservations = Reservation.objects.filter(
            meeting_room__id=meeting_room_id,
            time_from__lte=time_to,
            time_to__gte=time_from,
        )
        if reservations:
            raise serializers.ValidationError(error_codes.ROOM_ALREADY_BOOKED_FOR_CHOSEN_PERIOD)
        return data
