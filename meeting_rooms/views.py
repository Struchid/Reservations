from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MeetingRoomSerializer
from .models import MeetingRoom


class MeetingRoomViews(APIView):
    def post(self, request):
        serializer = MeetingRoomSerializer(data=request.data)
        if serializer.is_valid() and \
                not int(request.data.get('capacity')) == 0:
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data, },
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'data': serializer.errors, },
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                room = MeetingRoom.objects.get(id=id)
            except MeetingRoom.DoesNotExist:
                return Response(
                    {
                        'status': 'error',
                        'data': f'Meeting room with id {id} not found'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = MeetingRoomSerializer(room)
            return Response({'status': 'success', 'data': serializer.data},
                            status=status.HTTP_200_OK)

        meeting_rooms = MeetingRoom.objects.all()
        serializer = MeetingRoomSerializer(meeting_rooms, many=True)
        return Response({'status': 'success', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        room = get_object_or_404(MeetingRoom, id=id)
        room.delete()
        return Response({'status': 'success', 'data': 'Room Deleted'})
