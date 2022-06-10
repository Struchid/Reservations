from django.db import models
from django.utils import timezone


class BaseAbstractClass(models.Model):
    description = models.TextField(max_length=400, null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        abstract = True


def get_default_reservation_end_time() -> timezone:
    return timezone.now() + timezone.timedelta(hours=1)
