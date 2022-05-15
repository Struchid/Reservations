from django.contrib import admin

from .models import MeetingRoom, Reservation, User

admin.site.register(User)
admin.site.register(MeetingRoom)
admin.site.register(Reservation)
