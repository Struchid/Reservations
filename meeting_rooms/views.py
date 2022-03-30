from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MeetingRoomSerializer
from .models import MeetingRoom


class MeetingRoomViews(APIView):
    def post(self, request):
        serializer = MeetingRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data, }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'data': serializer.errors, }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, room_id=None):
        if room_id:
            room = MeetingRoom.objects.get(id=room_id)
            serializer = MeetingRoomSerializer(room)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

        meeting_rooms = MeetingRoom.objects.all()
        serializer = MeetingRoomSerializer(meeting_rooms, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, room_id=None):
        room = get_object_or_404(MeetingRoom, id=room_id)
        room.delete()
        return Response({'status': 'success', 'data': 'Room Deleted'})

