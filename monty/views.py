from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.shortcuts import render
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def home_page(request):
    return render(request, "home.html")


def signin_page(request):
    return render(request, "account/login.html")


def logout_page(request):
    return render(request, "account/logout.html")


def signup_page(request):
    return render(request, "account/signup.html")


def reset_password(request):
    return render(request, "account/password_reset.html")
