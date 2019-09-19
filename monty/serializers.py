from rest_framework import serializers
from monty.models import Profile, User, Dictionary, Theme, Word, Test


class DictionarySerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get("owner", None):
            raise serializers.ValidationError("Owner is not found")
        return data

    class Meta:
        model = Dictionary
        fields = (
            "id",
            "owner",
            "native_language",
            "foreign_language",
            "dictionary_name",
        )


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "theme_name", "dictionary")


class WordSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Word
        fields = ("id", "native_word", "foreign_word", "dictionary", "theme")


class TestSerializer(serializers.ModelSerializer):
    result = serializers.FloatField()
    test_date = serializers.DateTimeField()

    class Meta:
        model = Test
        fields = ("id", "result", "test_date")


class ProfileSerializer(serializers.ModelSerializer):
    dictionaries = DictionarySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ("native_language", "dictionaries")

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.players = validated_data
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        profile = instance.profile

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        profile.native_language = profile_data.get(
            "native_language", profile.native_language
        )
        profile.dictionary = profile_data.get("dictionary", profile.dictionaries)
        profile.save()

        return instance
