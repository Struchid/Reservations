from django.db import models
from django.utils import timezone


class MeetingRoom(models.Model):
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


class User(models.Model):
    username = models.CharField(max_length=100)

    class Meta:
        db_table = 'user'


class Reservation(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    time_from = models.DateTimeField(default=timezone.now)
    time_to = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservation'
