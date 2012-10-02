from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'span3', 'placeholder': 'Email address'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField()


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'span4'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'span4'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'span4'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'span4'}), required=True)
