# from django.views.generic import TemplateView
from django.shortcuts import render

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


# class FacebookLogin(TemplateView):
#     template_name = "facebook_auth.html"


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def facebook_auth(request):
    return render(request, "facebook_auth.html")


def signin_page(request):
    return render(request, "login.html")


def signup_page(request):
    return render(request, "registration.html")
