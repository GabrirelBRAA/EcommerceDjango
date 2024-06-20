from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", min_length=8, widget=forms.PasswordInput)

#TODO use only one password and add the function to see the written one
class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        special_characters = '!@#$%&()-_[]{};:"./<>?'
        if not any(ch in password for ch in special_characters):
            raise ValidationError("password must contain at least one special character!")
        if not any(ch.isdigit() for ch in password):
            raise ValidationError("password must contain at least one number!")
        if not any(ch.isalpha() for ch in password):
            raise ValidationError("password must contain at least one letter!")
        return password

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise ValidationError("password and confirm password do not match!")
