from django.urls import path, include
from rest_framework import routers

from .views import MeetingRoomViewSet, ReservationViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('meeting_rooms', MeetingRoomViewSet)
router.register('reservation', ReservationViewSet)
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
