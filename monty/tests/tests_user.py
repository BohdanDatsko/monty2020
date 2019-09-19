from rest_framework import status
from rest_framework.test import APITestCase
from monty.models import User


class UserAPITest(APITestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            "username": "test",
            "email": "test@test.com",
            "password": "test",
        }

        data = {
            "username": "test",
            "email": "test@test.com",
            "password": "test",
            "first_name": "first name",
            "last_name": "last name",
            "profile": {"native_language": "aa"},
        }

        self.user_create = self.client.post("/monty/users/", data, format="json")
        self.client.force_login(User.objects.first())

    def test_create_user(self):
        data = {
            "username": "test_api",
            "email": "test_api@test.com",
            "password": "test_api",
            "first_name": "first name",
            "last_name": "last name",
            "profile": {"native_language": "aa"},
        }

        response = self.client.post("/monty/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_list_user(self):
        get_response = self.client.get("/monty/users/")
        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user(self):

        retrieve_response = self.client.get(
            path="/monty/users/{pk}/".format(pk=User.objects.get(username="test").pk)
        )
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

    def test_partial_update_user(self):
        update_data = {
            "first_name": "FIRST NAME",
            "last_name": "LAST NAME",
            "profile": {"native_language": "ab"},
        }

        update_response = self.client.patch(
            path="/monty/users/{pk}/".format(pk=User.objects.get(username="test").pk),
            data=update_data,
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        update_data = {
            "username": "test",
            "email": "test_123@test.com",
            "password": "test",
            "first_name": "FIRST NAME",
            "last_name": "LAST NAME",
            "profile": {"native_language": "ab"},
        }

        update_response = self.client.put(
            path="/monty/users/{pk}/".format(pk=User.objects.get(username="test").pk),
            data=update_data,
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_destroy_user(self):
        update_response = self.client.delete(
            path="/monty/users/{pk}/".format(pk=User.objects.get(username="test").pk),
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
