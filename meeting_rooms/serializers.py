from rest_framework import serializers, status

from .models import MeetingRoom, Reservation, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'

    def validate(self, data):
        if data.get('capacity') <= 0:
            message = 'Capacity of the room must be a positive integer'
            return {'non_field_errors': [message], 'status_code': status.HTTP_400_BAD_REQUEST}
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
            message = 'Room is already booked for the requested period'
            return {'non_field_errors': [message], 'status_code': status.HTTP_400_BAD_REQUEST}
        return data
