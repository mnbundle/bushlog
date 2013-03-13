from django import forms


class NumberInput(forms.TextInput):
    input_type = 'number'


class EmailInput(forms.TextInput):
    input_type = 'email'
