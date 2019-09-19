from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from monty.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"^users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("monty/", include((router.urls, "monty"))),
    path("api/", include("api.urls", namespace="api_v1_monty")),
    #  Authentication
    path("auth/", include(("rest_auth.urls", "monty"), namespace="authentication")),
]
