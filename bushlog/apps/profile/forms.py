from django import forms
from django.core.urlresolvers import reverse_lazy

from bushlog import widgets
from bushlog.apps.location.models import Country
from bushlog.apps.profile.models import UserProfile, User
from bushlog.utils import choices


class SignInForm(forms.Form):
    username_email = forms.CharField(
        widget=widgets.EmailInput(attrs={'class': 'span12', 'placeholder': 'Username / Email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span12', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(required=False)


class SignUpModelForm(forms.ModelForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
            'class': 'span3 required',
            'minlength': 4,
            'remote': reverse_lazy('profile:validate', args=['unique'])
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3 required', 'equalTo': '#id_signup-password', 'minlength': 8})
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'span3 required',
                    'minlength': 4,
                    'remote': reverse_lazy('profile:validate', args=['unique'])
                }
            ),
            'email': widgets.EmailInput(
                attrs={'class': 'span3 required email ', 'remote': reverse_lazy('profile:validate', args=['unique'])}
            ),
            'password': forms.PasswordInput(attrs={'class': 'span3 required validpassword', 'minlength': 8}),
        }

    def clean(self):
        cleaned_data = super(SignUpModelForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data


class UpdateModelForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'span3 required',
                'minlength': 4,
                'remote': reverse_lazy('profile:validate', args=['unique'])
            }
        ),
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-modal-inline', 'placeholder': 'First name'}), max_length=30, required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-modal-inline', 'placeholder': 'Last name'}), max_length=30, required=False
    )
    email = forms.EmailField(
        widget=widgets.EmailInput(
            attrs={'class': 'span3 required email', 'remote': reverse_lazy('profile:validate', args=['unique'])}
        ),
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ['biography', 'gender', 'birth_date', 'country']
        widgets = {
            'biography': forms.Textarea(attrs={'class': 'span3', 'rows': 3, 'maxlength': 250}),
            'gender': forms.Select(attrs={'class': 'span3'}, choices=choices(['Male', 'Female'])),
            'birth_date': forms.DateInput(attrs={'readonly': 'readonly'}, format='%d/%m/%Y'),
            'country': forms.Select(
                attrs={'class': 'span3'}, choices=tuple([(obj.id, obj.name) for obj in Country.objects.all()])
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateModelForm, self).__init__(*args, **kwargs)

        # initialise the user fields with instance data
        if self.instance:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        super(UpdateModelForm, self).save(*args, **kwargs)

        # save the extra user data
        if self.instance:
            self.instance.user.username = self.cleaned_data.get('username')
            self.instance.user.first_name = self.cleaned_data.get('first_name')
            self.instance.user.last_name = self.cleaned_data.get('last_name')
            self.instance.user.email = self.cleaned_data.get('email')
            self.instance.user.save()


class AvatarModelForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'uk-input input',
                'data-upload-url': reverse_lazy('profile:avatar'),
                'data-max-file-size': '5mb',
                'data-file-resize': '{"width": 640, "height": 480, "quality": 90}'
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(
                attrs={
                    'class': 'uk-input input',
                    'data-upload-url': reverse_lazy('profile:avatar'),
                    'data-max-file-size': '5mb',
                    'data-file-resize': '{"width": 640, "height": 480, "quality": 90}'
                }
            )
        }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=widgets.EmailInput(
            attrs={'class': 'span3 required email', 'remote': reverse_lazy('profile:validate', args=['exists'])}
        ),
        required=True
    )


class ResendActivationForm(forms.Form):
    email = forms.EmailField(
        widget=widgets.EmailInput(
            attrs={'class': 'span3 required email', 'remote': reverse_lazy('profile:validate', args=['exists'])}
        ),
        required=True
    )
