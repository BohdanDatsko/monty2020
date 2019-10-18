from django.contrib.auth import get_user_model
from rest_framework import serializers

from monty.models import Dictionary, Theme, Word, Test

User = get_user_model()


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = (
            "id",
            "owner",
            "native_language",
            "foreign_language",
            "dictionary_name",
        )

    def validate(self, data):
        if not data.get("owner", None):
            raise serializers.ValidationError("Owner is not found")
        return data


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "theme_name", "dictionary")


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ("id", "native_word", "foreign_word", "dictionary", "theme")

    def validate(self, data):
        if data.get("theme", None):
            if data.get("theme").dictionary != data.get("dictionary", None):
                raise serializers.ValidationError("Theme dictionary != dictionary")
        elif data.get("dictionary", None):
            try:
                data["theme"] = Theme.objects.get(
                    theme_name="Default Theme", dictionary=data.get("dictionary")
                )
            except Theme.DoesNotExist:
                data["theme"] = Theme.objects.create(
                    theme_name="Default Theme", dictionary=data.get("dictionary")
                )
        else:
            raise serializers.ValidationError("data not valid")
        return data


class TestSerializer(serializers.ModelSerializer):
    dictionary = DictionarySerializer()
    themes = ThemeSerializer(many=True)
    words = WordSerializer(many=True)
    result = serializers.FloatField()
    test_date = serializers.DateTimeField()

    class Meta:
        model = Test
        fields = "__all__"
