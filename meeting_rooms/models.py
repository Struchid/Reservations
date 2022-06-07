from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class BaseAbstractClass(models.Model):
    description = models.TextField(max_length=400, null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        abstract = True


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


def get_default_reservation_end_time() -> timezone:
    return timezone.now() + timezone.timedelta(hours=1)


class Reservation(BaseAbstractClass):
    meeting_room = models.ForeignKey(MeetingRoom, related_name='reservations', on_delete=models.CASCADE)
    time_from = models.DateTimeField(default=timezone.now)
    time_to = models.DateTimeField(default=get_default_reservation_end_time)
    organizer = models.ForeignKey(User, related_name='organizer', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participations')

    class Meta:
        db_table = 'reservation'
