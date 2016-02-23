#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django import forms
from django.conf import settings

from projects.models import Project


class NewProjectForm(forms.Form):

    error_css_class = 'error'

    name = forms.CharField(max_length=255, label='Nazwa projektu')
    city = forms.CharField(max_length=128, label='Miasto')
    street = forms.CharField(max_length=128, label='Ulica')
    postcode = forms.CharField(max_length=6, label='Kod pocztowy')
    number = forms.CharField(max_length=24, label='Numer')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        try:
            Project.objects.get(name=name)
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError("Istnieje projekt o podanej nazwie")


    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')

        if not re.match(settings.POSTCODE_PATTERN, postcode):
            raise forms.ValidationError("Podaj kod pocztowy we właściwym formacie, np. 00-000")

        return postcode