# My Django Imports
from django import forms

from PAS_auth.models import (
    User,
)

# My App imports

class UserForm(forms.ModelForm):

    username = forms.CharField(help_text='Please enter student registration number',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    firstname = forms.CharField(help_text='Please enter student firstname', strip=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(help_text='Please enter student lastname',strip=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=False, help_text='Enter a valid email address',empty_value=None, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=False, help_text='Enter a valid phone number', strip=True, empty_value=None, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone != None:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone Number Already taken!')

        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username.upper().strip()).exists():
            raise forms.ValidationError('Registration Number already existing!')

        return username

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'phone', 'email')
