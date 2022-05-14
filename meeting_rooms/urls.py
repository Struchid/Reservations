from django.urls import path, include
from rest_framework import routers

from .views import MeetingRoomViewSet, ReservationViewSet


router = routers.DefaultRouter()
router.register('meeting_rooms', MeetingRoomViewSet)
router.register('reservation', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
