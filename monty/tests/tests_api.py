from django.utils import timezone
from api.views import TestList, TestDetail
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from monty.models import Profile, Dictionary, Theme, Word
from rest_framework.test import APITestCase, APIRequestFactory, APIClient


class DictionaryListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create(self):
        response = self.client.post(
            self.uri,
            {
                "owner": self.owner.id,
                "native_language": "uk",
                "foreign_language": "en",
                "dictionary_name": "En-Uk",
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class DictionaryDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk",
            native_language="en",
            foreign_language="uk",
            owner=self.owner,
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_retrieve(self):
        response = self.client.get(self.uri + str(self.test_dictionary.pk) + "/")
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            self.uri + str(self.test_dictionary.pk) + "/",
            {
                "owner": self.owner.id,
                "native_language": "uk",
                "foreign_language": "en",
                "dictionary_name": "Uk-En",
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy(self):
        response = self.client.delete(
            self.uri + str(self.test_dictionary.pk) + "/",
            {
                "owner": self.owner.id,
                "native_language": "uk",
                "foreign_language": "en",
                "dictionary_name": "Uk-En",
            },
        )
        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )


class ThemeListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_list(self):
        response = self.client.get(self.uri + str(self.test_dictionary.pk) + "/themes/")
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create(self):
        response = self.client.post(
            self.uri + str(self.test_dictionary.pk) + "/themes/",
            {"dictionary": self.test_dictionary.id, "theme_name": "Detective Comics"},
        )
        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class ThemeDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_retrieve(self):
        response = self.client.get(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/"
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/",
            {"dictionary": self.test_dictionary.id, "theme_name": "Vertigo"},
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy(self):
        response = self.client.delete(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/",
            {"dictionary": self.test_dictionary.id, "theme_name": "Vertigo"},
        )
        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )


class WordListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.test_word = Word.objects.create(
            native_word="{blablabla}",
            foreign_word="{блаблабла}",
            dictionary=self.test_dictionary,
            theme=self.test_theme,
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_list(self):
        response = self.client.get(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/words/"
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create(self):
        response = self.client.post(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/words/",
            {
                "native_word": "{blablabla}",
                "foreign_word": "{блаблабла}",
                "dictionary": self.test_dictionary.id,
                "theme": self.test_theme.id,
            },
        )
        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class WordDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.user = self.setup_user()
        self.owner = self.setup_profile(self.user)
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.test_word = Word.objects.create(
            native_word="{blablabla}",
            foreign_word="{блаблабла}",
            dictionary=self.test_dictionary,
            theme=self.test_theme,
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    @staticmethod
    def setup_profile(user):
        return Profile.objects.create(user=user, native_language="uk")

    def test_retrieve(self):
        response = self.client.get(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/words/"
            + str(self.test_word.pk)
            + "/"
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/words/"
            + str(self.test_word.pk)
            + "/",
            {
                "native_word": "ololololo",
                "foreign_word": "ололололо",
                "dictionary": self.test_dictionary.id,
                "theme": self.test_theme.id,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy(self):
        response = self.client.delete(
            self.uri
            + str(self.test_dictionary.pk)
            + "/themes/"
            + str(self.test_theme.pk)
            + "/words/"
            + str(self.test_word.pk)
            + "/",
            {
                "native_word": "{ololololo}",
                "foreign_word": "{ололололо}",
                "dictionary": self.test_dictionary.id,
                "theme": self.test_theme.id,
            },
        )
        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )


class TestTestViews(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TestList.as_view({"get": "list"})
        self.view1 = TestDetail.as_view()
        self.uri = "/api/tests"
        self.uri1 = "/api/tests/32/"
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            "test", email="testuser@test.com", password="test"
        )

    def test_list(self):
        request = self.factory.get(
            self.uri, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_details(self):
        request = self.factory.post(
            self.uri1,
            {"result": 47, "test_date": timezone.now()},
            HTTP_AUTHORIZATION="Token {}".format(self.token.key),
        )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )
