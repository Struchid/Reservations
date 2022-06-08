from datetime import timedelta

from django.urls import reverse
from model_bakery.baker import make
from rest_framework import status

from .models import MeetingRoom, User, Reservation
from .serializers import MeetingRoomSerializer
from meeting_rooms.utils.error_codes import Errors as errors
from meeting_rooms.utils.tests_utils import BaseTestCase


class MeetingRoomTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.payload_valid = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": 30,
        }
        self.payload_without_custom_name = {
            "room_number": "2015",
            "capacity": 30,
        }
        self.payload_without_required_field = {
            'custom_name': 'Mordor',
            "capacity": 30,
        }
        self.payload_capacity_zero = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": 0,
        }
        self.payload_capacity_negative = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": -30,
        }
        self.serializer = MeetingRoomSerializer(data=self.payload_capacity_zero)
        self.meeting_room = make(MeetingRoom, room_number='1', capacity=30)

    # POST
    def test_post_valid_payload(self):
        response = self.client.post(reverse('meetingroom-list'), data=self.payload_valid, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        latest_meeting_room_number = MeetingRoom.objects.latest('id').room_number
        self.assertEqual(latest_meeting_room_number, self.payload_valid.get('room_number'))

    def test_post_payload_without_custom_name(self):
        response = self.client.post(reverse('meetingroom-list'), data=self.payload_without_custom_name, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertIsNone(MeetingRoom.objects.latest('id').custom_name)

    def test_post_payload_without_room_number(self):
        response = self.client.post(reverse('meetingroom-list'), data=self.payload_without_required_field, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())

    def test_post_payload_zero_quantity(self):
        response = self.client.post(reverse('meetingroom-list'), data=self.payload_capacity_zero, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(response.data['non_field_errors'][0], errors.CAPACITY_NOT_POSITIVE_INTEGER_ERROR)

    def test_post_payload_negative_capacity(self):
        response = self.client.post(reverse('meetingroom-list'), data=self.payload_capacity_negative, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(response.data['capacity'][0], 'Ensure this value is greater than or equal to 0.')

    # GET
    def test_request_get_all_meeting_rooms(self):
        response = self.client.get(reverse('meetingroom-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_request_get_single_meeting_room(self):
        response = self.client.get(reverse('meetingroom-detail', args=[self.meeting_room.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_request_get_single_meeting_room_invalid_id(self):
        invalid_id = str(self.meeting_room.id + 1)
        response = self.client.get(reverse('meetingroom-detail', args=[invalid_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.json())

    # DELETE
    def test_request_delete_record_valid(self):
        response = self.client.delete(reverse('meetingroom-detail', args=[self.meeting_room.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MeetingRoom.objects.filter(id=1).exists())

    def test_request_delete_record_invalid(self):
        invalid_id = MeetingRoom.objects.latest('id').id + 1
        response = self.client.delete(reverse('meetingroom-detail', args=[invalid_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.json())


class UserTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.users = make(User, _quantity=5)

    def test_get_user_created_reservations(self):
        user_created_reservations = 3
        make(Reservation, organizer=self.users[0], _quantity=user_created_reservations)
        make(Reservation, organizer=self.users[1], _quantity=2)
        response = self.client.get(reverse('user-created-reservations', args=[self.users[0].id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(len(response.data), user_created_reservations)

    def test_get_user_attended_reservations(self):
        quantity = 10
        make(Reservation, participants=[], _quantity=quantity)
        attended_reservations = quantity / 2
        reservations = Reservation.objects.all()
        for reservation in reservations[:attended_reservations]:
            reservation.participants.add(self.users[0])
        response = self.client.get(reverse('user-participated-reservations', args=[self.users[0].id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(len(response.data), attended_reservations)


class ReservationTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.meeting_room = make(MeetingRoom)
        self.reservation = make(Reservation, meeting_room=self.meeting_room)
        self.user = make(User)

    def test_reservation_does_not_intertwine(self):
        data = {
            'meeting_room': self.meeting_room.id,
            'time_from': self.reservation.time_from + timedelta(days=1),
            'time_to': self.reservation.time_to + timedelta(days=1),
            'organizer': self.user.id,
            'participants': [self.user.id]
        }
        response = self.client.post(reverse('reservation-list'), data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservation_intertwines(self):
        data = {
            'meeting_room': self.meeting_room.id,
            'time_from': self.reservation.time_from,
            'time_to': self.reservation.time_to,
            'organizer': self.user.id,
            'participants': [self.user.id]
        }
        response = self.client.post(reverse('reservation-list'), data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], errors.ROOM_ALREADY_BOOKED_FOR_CHOSEN_PERIOD)
