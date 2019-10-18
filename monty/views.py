from django.views.generic import TemplateView
from django.shortcuts import render


class FacebookLogin(TemplateView):
    template_name = "facebook_auth.html"


def signin_signup_page(request):
    return render(request, "index.html")
