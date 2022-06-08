# Generated by Django 4.0.5 on 2022-06-07 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_rooms', '0002_alter_reservation_organizer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='meeting_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations',
                                    to='meeting_rooms.meetingroom'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='participants',
            field=models.ManyToManyField(related_name='participations', to=settings.AUTH_USER_MODEL),
        ),
    ]
