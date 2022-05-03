from django.urls import path, include
from rest_framework import routers

from .views import MeetingRoomViewSet


router = routers.DefaultRouter()
router.register('meeting_rooms', MeetingRoomViewSet)

urlpatterns = [
    path('', include(router.urls))
]
