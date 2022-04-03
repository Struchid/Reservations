from django.urls import path
from .views import MeetingRoomViews

urlpatterns = [
    path('meeting_rooms/', MeetingRoomViews.as_view()),
    path('meeting_rooms/<int:id>', MeetingRoomViews.as_view())
]