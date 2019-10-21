from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from monty.views import FacebookLogin, signin_page, signup_page, home_page, reset_password, logout_page
from monty2019.swagger import get_swagger_view

docs_api_view = get_swagger_view(title="Docs API")


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", admin.site.urls),

    # User management
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("", home_page, name="home"),
    path("account/login/", signin_page, name="login"),
    path("account/logout/", logout_page, name="login"),
    path("account/signup/", signup_page, name="registration"),
    path("account/password/reset/", reset_password, name="registration"),
    path("", include("allauth.urls")),

    # API
    path("api/docs/", docs_api_view, name="docs_api"),
    path("api/", include("api.urls", namespace="api_v1_monty")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
