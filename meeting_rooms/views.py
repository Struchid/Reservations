from rest_framework import viewsets

from .serializers import MeetingRoomSerializer, ReservationSerializer
from .models import MeetingRoom, Reservation


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
