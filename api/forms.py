from django.forms.widgets import CheckboxSelectMultiple, Select
from monty.models import Test, Theme, Dictionary
from django import forms


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["dictionary", "themes"]

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields["dictionary"].widget = Select()
        self.fields["themes"].widget = CheckboxSelectMultiple()
        if kwargs.get("initial", None):
            user_id = kwargs.get("initial").get("user_id", None)
            self.fields["dictionary"].queryset = Dictionary.objects.filter(
                owner_id=user_id
            )
            self.fields["themes"].queryset = Theme.objects.filter(
                dictionary__owner_id=user_id
            )
        else:
            self.fields["dictionary"].queryset = Dictionary.objects.all()
            self.fields["themes"].queryset = Theme.objects.all()
