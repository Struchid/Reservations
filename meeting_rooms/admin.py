from django.contrib import admin
from django.db import transaction

from .models import MeetingRoom, Reservation, User


class UserAdmin(admin.ModelAdmin):
    actions = ['disassociate_user_from_reservations', ]

    @transaction.atomic
    def disassociate_user_from_reservations(self, request, queryset):
        """Deletes organized reservations and removes user from attended ones"""
        user = queryset.first()
        user_id = user.id
        organized_reservations = Reservation.objects.select_related(
            'organizer').filter(organizer__id=user_id)
        organized_reservations.delete()
        participated_in_reservations = Reservation.objects.prefetch_related(
            'participants').filter(participants__id=user_id)
        for reservation in participated_in_reservations:
            reservation.participants.remove(queryset.first())
            if not reservation.participants.all():
                reservation.delete()


admin.site.register(User, UserAdmin)
admin.site.register(MeetingRoom)
admin.site.register(Reservation)
