from django.contrib.auth.models import User
from django.db import models


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


class Reservation(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    time_from = models.TimeField()
    time_to = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservation'
