import json

from django.core import exceptions
from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from .models import MeetingRoom


ENDPOINT = '/api/meeting_rooms/'
CONTENT_TYPE = 'application/json'


class TestRequestPost(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cls_atomics = cls._enter_atomics()
        cls.payload_valid = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": 30,
        }
        cls.payload_without_custom_name = {
            "room_number": "2015",
            "capacity": 30,
        }
        cls.payload_without_required_field = {
            'custom_name': 'Mordor',
            "capacity": 30,
        }
        cls.payload_capacity_zero = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": 0,
        }
        cls.payload_capacity_negative = {
            "room_number": "2015",
            'custom_name': 'Mordor',
            "capacity": -30,
        }

    def test_00_post_valid_payload(self):
        # Test valid POST request -- valid payload
        response = self.client.post(
            ENDPOINT, json.dumps(self.payload_valid), content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Valid payload POST was not successful')

        # Test if the record was created
        meeting_room = MeetingRoom.objects.get(**self.payload_valid)
        self.assertEqual(
            bool(meeting_room), True, 'Meeting room was not created with POST'
        )

    def test_01_post_payload_without_custom_name(self):
        # Test valid POST request -- not required field not provided
        response = self.client.post(
            ENDPOINT, json.dumps(self.payload_without_custom_name),
            content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_02_post_payload_without_room_number(self):
        # Test invalid POST request -- required field not provided
        response = self.client.post(
            ENDPOINT, json.dumps(self.payload_without_required_field),
            content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_post_payload_zero_quantity(self):
        # Test invalid POST request -- capacity field zero
        # (which makes no sense for room capacity)
        response = self.client.post(
            ENDPOINT, json.dumps(self.payload_capacity_zero),
            content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_post_payload_negative_capacity(self):
        # Test invalid POST request -- negative capacity provided
        with self.assertRaises(IntegrityError):
            self.client.post(
                ENDPOINT, json.dumps(self.payload_capacity_negative),
                content_type=CONTENT_TYPE
            )


class TestRequestGet(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        MeetingRoom.objects.create(room_number='1', capacity=30)

    def test_05_request_get_all_meeting_rooms(self):
        # Test valid GET request -- all meeting rooms
        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_06_request_get_single_meeting_room(self):
        # Test valid GET request -- single meeting room
        id = MeetingRoom.objects.get(room_number='1').id
        response = self.client.get(ENDPOINT + f'{id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_07_request_get_single_meeting_room_invalid_id(self):
        # Test valid GET request -- object does not exist
        id = str(MeetingRoom.objects.latest('id').id + 1)
        response = self.client.get(ENDPOINT + f'{id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRequestDelete(APITestCase):
    def setUp(self):
        MeetingRoom.objects.create(room_number='1', capacity=30)

    def test_08_request_delete_record_valid(self):
        # Test valid DELETE request
        response = self.client.delete(ENDPOINT+'1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Will fail if object is found -- not deleted
        try:
            MeetingRoom.objects.get(id=1)
            self.fail('Record was not deleted')
        except exceptions.ObjectDoesNotExist:
            self.assertEqual(1, 1)

    def test_09_request_delete_record_invalid(self):
        # Test invalid DELETE request
        invalid_id = str(MeetingRoom.objects.latest('id').id + 1) + '/'
        response = self.client.delete(ENDPOINT+invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)