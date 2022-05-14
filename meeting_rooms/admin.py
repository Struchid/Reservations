from django.contrib import admin

from .models import MeetingRoom, Reservation


admin.site.register(MeetingRoom)
admin.site.register(Reservation)
