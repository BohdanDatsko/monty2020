from django.urls import path

from api.views import (
    DictionaryList,
    DictionaryDetail,
    ThemeList,
    ThemeDetail,
    WordList,
    WordDetail,
    TestList,
    TestDetail,
    handle_test_creation,
    check_test,

)

app_name = "api"

urlpatterns = [
    path("dictionaries/",
         DictionaryList.as_view({"get": "list"}),
         name="dictionaries"),
    path(
        "dictionaries/<int:pk>/",
        DictionaryDetail.as_view(),
        name="dictionary_detail"
    ),
    path(
        "dictionaries/<int:d_pk>/themes/",
        ThemeList.as_view({"get": "list"}),
        name="themes"
    ),
    path(
        "dictionaries/<int:d_pk>/themes/<int:pk>/",
        ThemeDetail.as_view(),
        name="theme_detail"
    ),
    path(
        "dictionaries/<int:d_pk>/themes/<int:t_pk>/words/",
        WordList.as_view({"get": "list"}),
        name="words",
    ),
    path(
        "dictionaries/<int:d_pk>/themes/<int:t_pk>/words/<int:pk>/",
        WordDetail.as_view(),
        name="word_detail"
    ),
    path("tests/", TestList.as_view({"get": "list"}), name="tests"),
    path("tests/<int:pk>/", TestDetail.as_view(), name="tests_detail"),
    path("test/", handle_test_creation, name="test_view"),
    path("test/check/<int:pk>/", check_test, name="test_view_check"),
]
