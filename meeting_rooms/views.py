from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MeetingRoomSerializer, ReservationSerializer, UserSerializer
from .models import MeetingRoom, Reservation, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], detail=True, url_path='created_reservations')
    def created_reservations(self, request, pk=None):
        queryset = Reservation.objects.select_related('organizer').filter(organizer__id=pk)
        # queryset = User.objects.get(id=pk).organizer.filter(organizer__id=pk)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='participated_reservations')
    def participated_reservations(self, request, pk=None):
        queryset = Reservation.objects.prefetch_related('participants').filter(participants__id=pk)
        # queryset = User.objects.get(id=pk).participations.filter(participants__id=pk)
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
