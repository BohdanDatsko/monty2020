from itertools import chain

from django.contrib.auth import get_user_model
from django.db.models import F, Q
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

    # def create(self, request):
    #     data = request.data
    #     dictionary = Dictionary.objects.get(dictionary_name=data["dictionary"])
    #     themes = Theme.objects.get(theme_name=data["theme"])
    #     themes_ids = [item.id for item in themes]
    #     all_words = Word.objects.filter(
    #         dictionary_id=dictionary.id, theme_id__in=themes_ids
    #     )
    #     excellent_words = all_words.filter(
    #         Q(quality__lte=100) & Q(quality__gt=50)
    #     ).order_by("-count")[:5]
    #     good_words = all_words.filter(Q(quality__lte=50) & Q(quality__gt=20)).order_by(
    #         "-count"
    #     )[:10]
    #     bad_words = all_words.filter(Q(quality__lte=20) & Q(quality__gte=0)).order_by(
    #         "-count"
    #     )[:10]
    #     words = list(chain(excellent_words, good_words, bad_words))
    #     test = Test()
    #     test.dictionary = dictionary
    #     test.result = 0
    #     test.save()
    #     test.themes.set(themes)
    #     test.words.set(words)
    #     test.save()
    #     return test
    #
    # def update(self, request):
    #     data = request.data
    #     temp_result = 0
    #     test = Test.objects.get(test_id=data["id"])
    #     right_words = [q for q in test.words.all()]
    #     all_words = Word.objects.all()
    #     for word in right_words:
    #         all_words.filter(id=word.id).update(
    #             count=F("count") + 1
    #         )  # Update word's count
    #         user_answer = [data["foreign_word"][a] for a in data["foreign_word"]]
    #         right_answer = word.native_word[0]
    #         if user_answer == right_answer:
    #             temp_result += 1
    #             all_words.filter(id=word.id).update(
    #                 quality=(F("quality") + 100) / 2
    #             )  # Increase word's quality
    #         else:
    #             all_words.filter(id=word.id).update(quality=(F("quality") + 0) / 2)
    #     if temp_result == 0:
    #         test.result = 0
    #     else:
    #         test.result = round((temp_result * 100) / len(right_words), 2)
    #     test.save()
