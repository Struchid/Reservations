from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import MeetingRoomSerializer
from .models import MeetingRoom


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('capacity') == 0:
            return Response({
                'status': 'error',
                'body': 'Capacity cannot be zero'
            }, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
