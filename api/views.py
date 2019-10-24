from itertools import chain

from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

from api.forms import TestForm
from monty.models import Dictionary, Theme, Word, Test
from monty.permissions import (
    IsDictOwnerOrAdmin,
    IsThemeOwnerOrAdmin,
    IsWordOwnerOrAdmin,
)
from monty.serializers import (
    DictionarySerializer,
    ThemeSerializer,
    WordSerializer,
    TestSerializer,
)


class DictionaryList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (IsDictOwnerOrAdmin, IsAuthenticated)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        "dictionary_name",
        "created_at",
        "native_language",
        "foreign_language",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DictionaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (IsDictOwnerOrAdmin, IsAuthenticated)


class ThemeList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = (IsThemeOwnerOrAdmin, IsAuthenticated)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["theme_name"]

    def perform_create(self, serializer):
        serializer.save(dictionary_id=self.kwargs.get("d_pk", None))

    def get_queryset(self):
        queryset = Theme.objects.filter(dictionary=self.kwargs.get("d_pk", None))
        return queryset


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = (IsThemeOwnerOrAdmin, IsAuthenticated)


class WordList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = (IsWordOwnerOrAdmin, IsAuthenticated)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["dictionary", "theme"]
    ordering_fields = ["native_word", "foreign_word"]

    def perform_create(self, serializer):
        serializer.save(dictionary_id=self.kwargs.get("d_pk", None))

    def get_queryset(self):
        queryset = Word.objects.filter(theme=self.kwargs.get("t_pk", None))
        return queryset


class WordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = (IsWordOwnerOrAdmin, IsAuthenticated)


class TestList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


def handle_test_creation(request):
    if request.method == "POST":  # If the form has been submitted...
        form = TestForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            # return HttpResponseRedirect('/thanks/') # Redirect after POST
            dictionary = form.cleaned_data.get("dictionary")
            themes = form.cleaned_data.get("themes")
            themes_ids = [item.id for item in themes]
            all_words = Word.objects.filter(
                dictionary_id=dictionary.id, theme_id__in=themes_ids
            )
            print(all_words)
            if len(all_words) == 0:
                return HttpResponse(
                    "Here's no words in this dictionary for this themes yet. Please choose another one."
                )
            else:
                excellent_words = all_words.filter(
                    Q(quality__lte=100) & Q(quality__gt=50)
                ).order_by("-count")[:5]
                good_words = all_words.filter(
                    Q(quality__lte=50) & Q(quality__gt=20)
                ).order_by("-count")[:10]
                bad_words = all_words.filter(
                    Q(quality__lte=20) & Q(quality__gte=0)
                ).order_by("-count")[:10]
                words = list(
                    chain(excellent_words, good_words, bad_words)
                )  # List of filtered words by quality and count
            test = Test()
            test.dictionary = dictionary
            test.result = 0
            test.save()
            test.themes.set(themes)
            test.words.set(words)
            test.save()
            # prepare words to json
            res_words = []
            for w in words:
                res_words.append(
                    {"fw": w.foreign_word[0], "nw": w.native_word[0], "id": w.id}
                )

            return render(
                request, "contact.html", {"test_id": test.id, "words": res_words}
            )
    else:
        form = TestForm(initial={"user_id": request.user.id})  # An unbound form

    return render(request, "contact.html", {"form": form})


def check_test(request, pk):
    if request.method == "POST":  # If the form has been submitted...
        temp_result = 0
        test = Test.objects.get(pk=pk)
        right_words = test.words.all()
        all_words = Word.objects.all()
        for word in right_words:
            all_words.filter(id=word.id).update(
                count=F("count") + 1
            )  # Update word's count
            user_answer = request.POST.get(word.foreign_word[0])
            right_answer = word.native_word[0]
            if user_answer == right_answer:
                temp_result += 1
                all_words.filter(id=word.id).update(
                    quality=(F("quality") + 100) / 2
                )  # Increase word's quality
            else:
                all_words.filter(id=word.id).update(quality=(F("quality") + 0) / 2)
        if temp_result == 0:
            test.result = 0
        else:
            test.result = round((temp_result * 100) / len(right_words), 2)
        test.save()
        return render(request, "contact.html", {"test_result": test.result})
    else:
        form = TestForm()  # An unbound form

    return render(request, "contact.html", {"form": form})
