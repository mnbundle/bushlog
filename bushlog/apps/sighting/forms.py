from datetime import datetime

from django import forms

from bushlog import widgets
from bushlog.apps.sighting.models import Sighting


class CreateForm(forms.ModelForm):
    image_ids = forms.CharField(widget=forms.HiddenInput(), required=False)
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    reserve_search = forms.CharField(widget=forms.TextInput(attrs={'class': 'span3 required'}))
    species_search = forms.CharField(widget=forms.TextInput(attrs={'class': 'span3 required'}))
    time_of_sighting = forms.TimeField(
        widget=forms.TimeInput(attrs={'readonly': 'readonly', 'class': 'required time'})
    )

    class Meta:
        model = Sighting
        fields = [
            'reserve', 'species', 'date_of_sighting', 'time_of_sighting', 'description', 'estimated_number', 'sex',
            'with_young', 'with_kill'
        ]
        widgets = {
            'reserve': forms.HiddenInput(),
            'species': forms.HiddenInput(),
            'date_of_sighting': forms.DateInput(attrs={'readonly': 'readonly', 'class': 'required localdate'}),
            'description': forms.Textarea(attrs={'class': 'span3', 'rows': 3, 'maxlength': 1000}),
            'estimated_number': widgets.NumberInput(attrs={'class': 'span3 number', 'autocomplete': 'off'}),
            'sex': forms.Select(attrs={'class': 'span3'})
        }

    def clean(self):
        cleaned_data = super(CreateForm, self).clean()

        # reformat the date to include the time
        date_of_sighting = cleaned_data.get('date_of_sighting')
        time_of_sighting = cleaned_data.get('time_of_sighting')
        cleaned_data['date_of_sighting'] = datetime(
            date_of_sighting.year,
            date_of_sighting.month,
            date_of_sighting.day,
            time_of_sighting.hour,
            time_of_sighting.minute
        )

        return cleaned_data

