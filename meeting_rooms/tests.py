import json

from django.test import TestCase
from django.urls import reverse
from model_bakery.baker import make
from rest_framework import serializers
from rest_framework import status

from .models import MeetingRoom, User, Reservation
from .serializers import MeetingRoomSerializer


CONTENT_TYPE = 'application/json'


class BaseTestCase(TestCase):
    pass


class RequestMeetingRoomPostTestCase(BaseTestCase):
    def setUp(self):
        self.endpoint = '/api/meeting_rooms/'
        self.cls_atomics = self._enter_atomics()
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

    # def test_post_valid_payloadload(self):
    #     # Test valid POST request -- valid payload
    #     response = self.client.post(self.endpoint, json.dumps(self.payload_valid), content_type=CONTENT_TYPE)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
    #     latest_meeting_room_number = MeetingRoom.objects.latest('id').room_number
    #     self.assertEqual(latest_meeting_room_number, self.payload_valid.get('room_number'))
    #
    # def test_post_payload_without_custom_name(self):
    #     # Test valid POST request -- not required field not provided
    #     response = self.client.post(
    #         self.endpoint, json.dumps(self.payload_without_custom_name), content_type=CONTENT_TYPE
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
    #     self.assertIsNone(MeetingRoom.objects.latest('id').custom_name)
    #
    # def test_post_payload_without_room_number(self):
    #     # Test invalid POST request -- required field not provided
    #     response = self.client.post(
    #         self.endpoint, json.dumps(self.payload_without_required_field), content_type=CONTENT_TYPE
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
    #
    # def test_post_payload_zero_quantity(self):
    #     # Test invalid POST request -- capacity field zero
    #     response = self.client.post(self.endpoint, json.dumps(self.payload_capacity_zero), content_type=CONTENT_TYPE)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
    #     print(response.__dict__)
    #     # self.assertEqual(response.non_field_errors, 'Capacity of the room must be a positive integer')
    #     self.assertFalse(self.serializer.is_valid())
    #
    # def test_post_payload_negative_capacity(self):
    #     # Test invalid POST request -- negative capacity provided
    #     response = self.client.post(
    #         self.endpoint, json.dumps(self.payload_capacity_negative), content_type=CONTENT_TYPE
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
    #     print(response.__dict__)
    #     # self.assertEqual(response.non_field_errors, 'Capacity of the room must be a positive integer')
    #     self.assertFalse(self.serializer.is_valid())

# class RequestMeetingRoomGetTestCase(BaseTestCase):
#     def setUp(self):
#         self.endpoint = '/api/meeting_rooms/'
#         self.meeting_room = make(MeetingRoom, room_number='1', capacity=30)
#
#     def test_request_get_all_meeting_rooms(self):
#         # Test valid GET request -- all meeting rooms
#         response = self.client.get(self.endpoint)
#         self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    # def test_request_get_single_meeting_room(self):
    #     # Test valid GET request -- single meeting room
    #     from meeting_rooms.urls import router
    #     # print(reverse('meetingroom-list', kwargs={'id': 1}))
    #     response = self.client.get(reverse('rooms-list', args=(1,)))  # TODO: Use reverse()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

#     def test_request_get_single_meeting_room_invalid_id(self):
#         # Test valid GET request -- object does not exist
#         id = str(self.meeting_room.id + 1)
#         # response = self.client.get(self.endpoint + f'{id}/')  # TODO: Use reverse()
#         print(id)
#         response = self.client.get(reverse('meetingroom-list', kwargs={'id': id}))  # TODO: Use reverse()
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.json())
#
#
# class RequestMeetingRoomDeleteTestCase(BaseTestCase):
#     def setUp(self):
#         self.endpoint = '/api/meeting_rooms/'
#         self.meeting_room = make(MeetingRoom, room_number='1', capacity=30)
#
#     def test_request_delete_record_valid(self):
#         # Test valid DELETE request
#         response = self.client.delete(self.endpoint + str(self.meeting_room.id) + '/')  # TODO: Use reverse()
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         # Will fail if object is found -- not deleted
#         self.assertFalse(MeetingRoom.objects.filter(id=1).exists())
#
#     def test_request_delete_record_invalid(self):
#         # Test invalid DELETE request
#         invalid_id = str(MeetingRoom.objects.latest('id').id + 1) + '/'  # TODO: Use reverse()
#         response = self.client.delete(self.endpoint+invalid_id)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.json())
#
#
# class CustomEndpointsTestCase(BaseTestCase):
#     def setUp(self):
#         self.users = make(User, _quantity=5)
#
#     def test_get_user_created_reservations(self):
#         user_created_reservations = 3
#         make(Reservation, organizer=self.users[0], _quantity=user_created_reservations)
#         make(Reservation, organizer=self.users[1], _quantity=2)
#         response = self.client.get(reverse('user-created-reservations', kwargs={'pk': self.users[0].id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
#         self.assertEqual(len(response.data), user_created_reservations)
#
#     def test_get_user_attended_reservations(self):
#         quantity = 10
#         make(Reservation, participants=[], _quantity=quantity)
#         attended_reservations = quantity / 2
#         reservations = Reservation.objects.all()
#         for reservation in reservations[:attended_reservations]:
#             reservation.participants.add(self.users[0])
#         response = self.client.get(reverse('user-participated-reservations', kwargs={'pk': self.users[0].id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
#         self.assertEqual(len(response.data), attended_reservations)
