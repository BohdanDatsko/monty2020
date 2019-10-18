from django.forms.widgets import CheckboxSelectMultiple
from monty.models import Test, Theme
from django import forms


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["dictionary", "themes"]

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields["themes"].widget = CheckboxSelectMultiple()
        self.fields["themes"].queryset = Theme.objects.all()
