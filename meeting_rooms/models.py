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
