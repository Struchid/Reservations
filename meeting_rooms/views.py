from rest_framework import viewsets

from .serializers import MeetingRoomSerializer
from .models import MeetingRoom


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
