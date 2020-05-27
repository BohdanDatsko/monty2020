import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from monty.models import Word, Theme, Dictionary, Test

User = get_user_model()


class WordTestModel(TestCase):
    """
        Test module for Word model
    """

    def setUp(self):
        self.test_user = mommy.make(User)

        dictionary_en_uk = Dictionary.objects.create(
            dictionary_name="English-Ukrainian", owner=self.test_user
        )

        theme_r = Theme.objects.create(theme_name="Water", dictionary=dictionary_en_uk)

        mommy.make(Word, native_word="{river}", foreign_word="{річка}", theme=theme_r)
        mommy.make(Word, native_word="{boat}", foreign_word="{човен}", theme=theme_r)

    def test_add_word(self):
        dictionary_en_uk = Dictionary.objects.get(
            dictionary_name="English-Ukrainian", owner=self.test_user
        )

        theme_r = Theme.objects.get(theme_name="Water", dictionary=dictionary_en_uk)

        word_river = Word.objects.get(native_word="{river}", theme=theme_r)
        word_boat = Word.objects.get(native_word="{boat}", theme=theme_r)

        self.assertEqual(
            word_river.get_translate(), "['river'] is translated as ['річка']."
        )
        self.assertEqual(
            word_boat.get_translate(), "['boat'] is translated as ['човен']."
        )

    def test_remove_word(self):
        word_river = Word.objects.get(native_word="{river}")
        word_boat = Word.objects.get(native_word="{boat}")

        word_river.delete()
        word_boat.delete()

        self.assertEqual(Word.objects.filter(native_word="{river}").count(), 0)
        self.assertEqual(Word.objects.filter(native_word="{boat}").count(), 0)


class ThemeTestModel(TestCase):
    """
        Test module for Theme model
    """

    def setUp(self):
        self.test_user = mommy.make(User)

        dictionary_en_uk = Dictionary.objects.create(
            dictionary_name="English-Ukrainian", owner=self.test_user
        )

        theme_r = Theme.objects.create(theme_name="Water", dictionary=dictionary_en_uk)

        Word.objects.create(
            native_word="{river}",
            foreign_word="{річка}",
            theme=theme_r,
            dictionary=dictionary_en_uk,
        )

    def test_add_theme_word(self):
        dictionary_en_uk = Dictionary.objects.get(
            dictionary_name="English-Ukrainian", owner=self.test_user
        )

        theme_r = Theme.objects.get(theme_name="Water", dictionary=dictionary_en_uk)

        river = Word.objects.get(theme=theme_r, dictionary=dictionary_en_uk)

        self.assertEqual(
            theme_r.get_theme_name(river.id), "['river'] belongs to Water theme."
        )

    def test_remove_theme_word(self):

        dictionary_en_uk = Dictionary.objects.get(
            dictionary_name="English-Ukrainian", owner=self.test_user
        )

        theme_r = Theme.objects.get(theme_name="Water", dictionary=dictionary_en_uk)

        river = Word.objects.get(theme=theme_r, dictionary=dictionary_en_uk)

        river.delete()

        self.assertEqual(river.theme.id, theme_r.id)


class DictionaryTestModel(TestCase):
    """
        Test module for Dictionary model
    """

    def setUp(self):
        self.test_user = mommy.make(User)

        Dictionary.objects.create(dictionary_name="English", owner=self.test_user)

    def test_add_dictionary_theme(self):

        test_dictionary = Dictionary.objects.get(
            dictionary_name="English", owner=self.test_user
        )

        test_theme = Theme.objects.create(
            theme_name="London", dictionary=test_dictionary
        )

        self.assertEqual(test_theme.dictionary.id, test_dictionary.id)

    def test_remove_dictionary_theme(self):
        test_dictionary = Dictionary.objects.get(
            dictionary_name="English", owner=self.test_user
        )

        Theme.objects.create(theme_name="London", dictionary=test_dictionary)

        test_theme = Theme.objects.get(theme_name="London", dictionary=test_dictionary)

        test_theme.delete()

        self.assertEqual(test_theme.dictionary.id, test_dictionary.id)


class TestTestModel(TestCase):
    """
        Class to test the model Test
    """

    def setUp(self):
        user_test = User.objects.create_user(
            username="test", email="test@user.com", password="foo"
        )
        dictionary_test = Dictionary.objects.create(
            dictionary_name="English", owner=user_test
        )
        mommy.make(Test, result=45, dictionary=dictionary_test)
        Test.objects.create(result=90, dictionary=dictionary_test)

    def test_add_result(self):
        test45 = Test.objects.get(result=45)
        test90 = Test.objects.get(result=90)

        self.assertEqual(test45.result, 45)
        self.assertEqual(test90.result, 90)

    def test_delete_result(self):
        res_45 = Test.objects.get(result=45)
        res_90 = Test.objects.get(result=90)

        res_45.delete()
        res_90.delete()

        self.assertEqual(Test.objects.filter(result=45).count(), 0)
        self.assertEqual(Test.objects.filter(result=90).count(), 0)

    def test_was_passed_recently_with_old_test(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_test = Test(test_date=time)
        self.assertIs(old_test.was_passed_recently(), False)

    def test_was_passed_recently_with_recent_test(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_test = Test(test_date=time)
        self.assertIs(recent_test.was_passed_recently(), True)
