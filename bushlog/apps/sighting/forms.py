from django import forms

from bushlog.apps.sighting.models import Sighting


class CreateForm(forms.ModelForm):
    class Meta:
        model = Sighting
