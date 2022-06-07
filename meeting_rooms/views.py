from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MeetingRoomSerializer, ReservationSerializer, UserSerializer
from .models import MeetingRoom, Reservation, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], detail=True, url_path='get_user_created_reservations', url_name='created-reservations')
    def get_user_created_reservations(self, request, pk=None):
        queryset = Reservation.objects.select_related('organizer').filter(organizer__id=pk)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['GET'], detail=True, url_path='get_user_attended_reservations', url_name='participated-reservations'
    )
    def get_user_attended_reservations(self, request, pk=None):
        queryset = Reservation.objects.prefetch_related('participants').filter(participants__id=pk)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
