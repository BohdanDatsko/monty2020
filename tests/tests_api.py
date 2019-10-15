from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from api.views import TestList, TestDetail
from monty.models import Dictionary, Theme, Word, Test

User = get_user_model()


class DictionaryListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/dictionaries/"
        self.owner = self.setup_user()
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

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
            format="json",
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
        self.owner = self.setup_user()
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk",
            native_language="en",
            foreign_language="uk",
            owner=self.owner,
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_retrieve(self):
        response = self.client.get("{0}{1}/".format(self.uri, self.test_dictionary.pk))
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            "{0}{1}/".format(self.uri, self.test_dictionary.pk),
            {
                "owner": self.owner.id,
                "native_language": "uk",
                "foreign_language": "en",
                "dictionary_name": "Uk-En",
            },
            format="json",
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
            "{0}{1}/".format(self.uri, self.test_dictionary.pk)
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
        self.owner = self.setup_user()
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_list(self):
        response = self.client.get(
            "{0}{1}/themes/".format(self.uri, self.test_dictionary.pk)
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
            "{0}{1}/themes/".format(self.uri, self.test_dictionary.pk),
            {"dictionary": self.test_dictionary.id, "theme_name": "Detective Comics"},
            format="json",
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
        self.owner = self.setup_user()
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_retrieve(self):
        response = self.client.get(
            "{0}{1}/themes/{2}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk
            )
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
            "{0}{1}/themes/{2}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk
            ),
            {"dictionary": self.test_dictionary.id, "theme_name": "Vertigo"},
            format="json",
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
            "{0}{1}/themes/{2}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk
            )
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
        self.owner = self.setup_user()
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_list(self):
        response = self.client.get(
            "{0}{1}/themes/{2}/words/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk
            )
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
            "{0}{1}/themes/{2}/words/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk
            ),
            {
                "native_word": ["blablabla"],
                "foreign_word": ["блаблабла"],
                "dictionary": self.test_dictionary.id,
                "theme": self.test_theme.id,
            },
            format="json",
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
        self.owner = self.setup_user()
        self.test_dictionary = Dictionary.objects.create(
            dictionary_name="En-Uk", owner=self.owner
        )
        self.test_theme = Theme.objects.create(
            theme_name="Detective Comics", dictionary=self.test_dictionary
        )
        self.test_word = Word.objects.create(
            native_word=["blablabla"],
            foreign_word=["блаблабла"],
            dictionary=self.test_dictionary,
            theme=self.test_theme,
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_retrieve(self):
        response = self.client.get(
            "{0}{1}/themes/{2}/words/{3}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk, self.test_word.pk
            )
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
            "{0}{1}/themes/{2}/words/{3}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk, self.test_word.pk
            ),
            {
                "native_word": ["ololololo"],
                "foreign_word": ["ололололо"],
                "dictionary": self.test_dictionary.id,
                "theme": self.test_theme.id,
            },
            format="json",
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
            "{0}{1}/themes/{2}/words/{3}/".format(
                self.uri, self.test_dictionary.pk, self.test_theme.pk, self.test_word.pk
            )
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
        self.uri = "/api/tests/"
        self.uri1 = "/api/tests/32/"
        self.owner = self.setup_user()
        self.example_test = Test.objects.create(result=53, test_date=timezone.now())
        self.token = Token.objects.create(user=self.owner)
        self.token.save()

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne",
            email="batman@batcave.com",
            password="Martha",
            native_language="uk",
        )

    def test_list(self):
        request = self.factory.get(
            self.uri, HTTP_AUTHORIZATION="Token {}".format(self.token.key)
        )
        request.user = self.owner
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_details(self):
        request = self.factory.get(
            "{0}{1}/".format(self.uri, self.example_test.pk),
            HTTP_AUTHORIZATION="Token {}".format(self.token.key),
        )
        request.user = self.owner
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )
