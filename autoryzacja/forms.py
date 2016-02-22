#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from autoryzacja.models import PipesUser

my_default_errors = {
    'required': 'To pole jest wymagane',
    'invalid': 'Wprowadź prawidłową wartość'
}


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Adres email', max_length=100, error_messages=my_default_errors)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput, error_messages=my_default_errors)
    username = forms.CharField(required=False, max_length=10, error_messages=my_default_errors)


class RegisterForm(forms.Form):

    error_css_class = 'error'

    email = forms.EmailField(label='Adres email',
                             max_length=100,
                             error_messages=my_default_errors)

    first_name = forms.CharField(label='Imię',
                                 max_length=32,
                                 error_messages=my_default_errors)

    last_name = forms.CharField(label='Nazwisko',
                                max_length=64,
                                error_messages=my_default_errors)

    password = forms.CharField(label='Hasło',
                               max_length=100,
                               widget=forms.PasswordInput,
                               error_messages=my_default_errors)

    password2 = forms.CharField(label='Powtórz hasło',
                                max_length=100,
                                widget=forms.PasswordInput,
                                error_messages=my_default_errors)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            PipesUser.objects.get(email=email)
        except PipesUser.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("Istnieje użytkownik o podanym adresie email")

    def clean_password2(self):
        password_first = self.cleaned_data.get("password")
        password_second = self.cleaned_data.get("password2")

        if not password_first or not password_second or password_first != password_second:
            raise forms.ValidationError("Hasła nie są takie same")
        validate_password(password_second)

        return password_second