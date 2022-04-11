from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import MeetingRoomSerializer
from .models import MeetingRoom


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
