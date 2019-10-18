from django.views.generic import TemplateView


class FacebookLogin(TemplateView):
    template_name = "facebook_auth.html"
