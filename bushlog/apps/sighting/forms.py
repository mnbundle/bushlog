from django import forms

from bushlog import widgets
from bushlog.apps.sighting.models import Sighting
from bushlog.utils import choices


class CreateForm(forms.ModelForm):
    image_ids = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sighting
        fields = [
            'reserve', 'species', 'date_of_sighting', 'description', 'estimated_number', 'sex', 'with_young',
            'with_kill'
        ]
        widgets = {
            'reserve': forms.Select(attrs={'class': 'span3 required'}),
            'species': forms.Select(attrs={'class': 'span3 required'}),
            'date_of_sighting': forms.DateInput(attrs={'readonly': 'readonly', 'class': 'required date'}, format='%d/%m/%Y'),
            'description': forms.Textarea(attrs={'class': 'span3', 'rows': 3, 'maxlength': 1000}),
            'estimated_number': widgets.NumberInput(attrs={'class': 'span3 number'}),
            'sex': forms.Select(attrs={'class': 'span3'})
        }

    def save(self, *args, **kwargs):
        super(CreateForm, self).save(*args, **kwargs)
