import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from languages.fields import LanguageField

User = get_user_model()


class Dictionary(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dictionaries"
    )
    native_language = LanguageField()
    foreign_language = LanguageField()
    dictionary_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dictionary"
        verbose_name_plural = "Dictionaries"

    def __str__(self):
        return "{0}".format(self.dictionary_name)

    def get_dictionary_name(self, theme_id):
        theme = Theme.objects.get(id=theme_id)
        return f"{theme.theme_name} belongs to {self.dictionary_name} dictionary."


class Theme(models.Model):
    theme_name = models.CharField(max_length=100)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    def __str__(self):
        return f"{self.theme_name}"

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def clean(self):
        if not self.dictionary:
            raise ValidationError("Dictionary does not exist")

    def get_user(self):
        user = self.dictionary.owner
        return user

    def get_theme_name(self, word_id):
        word = Word.objects.get(id=word_id)
        return f"{word.native_word} belongs to {self.theme_name} theme."


class Word(models.Model):
    native_word = ArrayField(models.CharField(max_length=100))
    foreign_word = ArrayField(models.CharField(max_length=100))
    quality = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        related_name="native_word",
        blank=False,
        null=True,
    )

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return f"{self.native_word} - {self.foreign_word}"

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def clean(self):
        if not self.dictionary:
            raise ValidationError("Dictionary does not exist")
        elif not self.theme:
            raise ValidationError("Theme does not exist")

    def get_user(self):
        user = self.theme.dictionary.owner
        return user

    def get_translate(self):
        return f"{self.native_word} is translated as {self.foreign_word}."


class Test(models.Model):
    themes = models.ManyToManyField(Theme)
    words = models.ManyToManyField(Word)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, null=True)
    result = models.FloatField()
    test_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return f"{self.id}"

    def was_passed_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.test_date <= now
