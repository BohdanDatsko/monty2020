from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

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
