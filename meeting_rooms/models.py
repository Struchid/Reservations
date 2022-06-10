from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from meeting_rooms.utils.models import BaseAbstractClass, get_default_reservation_end_time


class User(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class MeetingRoom(BaseAbstractClass):
    room_number = models.CharField(max_length=16, unique=True)
    custom_name = models.CharField(max_length=32, null=True, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        if self.custom_name:
            name = f'{self.room_number} - {self.custom_name}'
        else:
            name = f'{self.room_number}'
        return name

    class Meta:
        db_table = 'meeting_room'


class Reservation(BaseAbstractClass):
    meeting_room = models.ForeignKey(MeetingRoom, related_name='reservations', on_delete=models.CASCADE)
    time_from = models.DateTimeField(default=timezone.now)
    time_to = models.DateTimeField(default=get_default_reservation_end_time)
    organizer = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participations')

    class Meta:
        db_table = 'reservation'
