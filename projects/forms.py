#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django import forms
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from projects.models import Project, Prefabricate
from pipes_types.models import PipeMark, PipeRightEnd, PipeLeftEnd, PipeColor, PipeDiameter, PipeType, PipeOutflow, PipeOutflowSize


class EditProjectForm(forms.Form):

    error_css_class = 'error'

    name = forms.CharField(max_length=255, label='Nazwa projektu')
    city = forms.CharField(max_length=128, label='Miasto')
    street = forms.CharField(max_length=128, label='Ulica')
    postcode = forms.CharField(max_length=6, label='Kod pocztowy')
    number = forms.CharField(max_length=24, label='Numer')
    #
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #
    #     try:
    #         Project.objects.get(name=name)
    #     except Project.DoesNotExist:
    #         return name
    #     raise forms.ValidationError("Istnieje projekt o podanej nazwie")


    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')

        if not re.match(settings.POSTCODE_PATTERN, postcode):
            raise forms.ValidationError("Podaj kod pocztowy we właściwym formacie, np. 00-000")

        return postcode


class NewProjectForm(EditProjectForm):

    def clean_name(self):
        name = self.cleaned_data.get('name')

        try:
            Project.objects.get(name=name)
        except Project.DoesNotExist:
            return name
        raise forms.ValidationError("Istnieje projekt o podanej nazwie")


class PipeEndModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        image = conditional_escape(obj.image.url)

        label = "<img src='{}' title='{}'/>".format(image, obj.name)

        return mark_safe(label)


class AddPrefabricateForm(forms.Form):

    error_css_class = 'error'

    diameter = forms.ModelChoiceField(PipeDiameter.objects.filter(available=True), label='Średnica')
    type = forms.ModelChoiceField(PipeType.objects.filter(available=True), label='Rodzaj rury',
                                  widget=forms.Select(attrs={'onChange': 'getColorEnabled()'}))
    mark = forms.CharField(label='Oznaczenie')
    color = forms.ModelChoiceField(PipeColor.objects.filter(available=True), label='Kolor', required=False)
    left_end = PipeEndModelChoiceField(PipeLeftEnd.objects.filter(available=True), label='Zakończenie lewe',
                                       widget=forms.RadioSelect,
                                       empty_label=None)
    right_end = PipeEndModelChoiceField(PipeRightEnd.objects.filter(available=True), label='Zakończenie prawe',
                                        widget=forms.RadioSelect,
                                        empty_label=None)
    quantity = forms.TypedChoiceField(choices=[(val, str(val)) for val in range(1, 16)], coerce=int, label='Ilość')

    def clean(self):
        type = self.cleaned_data.get('type')
        color = self.cleaned_data.get('color')

        if type is None:
            return

        if not type.color_allowed and color:
            self.add_error('type', 'Dla danego typy rury kolor jest niedostępny')


class OutflowManipulateFormAdd(forms.Form):

    prefabricate_id = forms.IntegerField()
    outflow_id = forms.IntegerField()
    index = forms.IntegerField()

    def clean_prefabricate_id(self):
        prefabricate_id = self.cleaned_data.get('prefabricate_id')

        try:
            Prefabricate.objects.get(id=prefabricate_id)
        except Prefabricate.DoesNotExist:
            raise forms.ValidationError("Prefabrykat nie istnieje")
        return prefabricate_id

    def clean_outflow_id(self):
        outflow_id = self.cleaned_data.get('outflow_id')

        try:
            outflow = PipeOutflow.objects.get(id=outflow_id)
        except PipeOutflow.DoesNotExist:
            raise forms.ValidationError("Odejście nie istnieje")

        if not outflow.available:
            raise forms.ValidationError("Odejście nie dostępne")
        return outflow_id


class OutflowManipulateFormDelete(forms.Form):

    prefabricate_id = forms.IntegerField()
    index = forms.IntegerField()

    def clean_prefabricate_id(self):
        prefabricate_id = self.cleaned_data.get('prefabricate_id')

        try:
            Prefabricate.objects.get(id=prefabricate_id)
        except Prefabricate.DoesNotExist:
            raise forms.ValidationError("Prefabrykat nie istnieje")
        return prefabricate_id


class OutflowDistanceManipulateForm(OutflowManipulateFormDelete):

    distance = forms.IntegerField(min_value=0)


class OutflowSizeManipulateForm(OutflowManipulateFormDelete):

    size = forms.ModelChoiceField(PipeOutflowSize.objects.filter(available=True))


class ProjectCommentForm(forms.Form):

    project_id = forms.IntegerField()
    comment = forms.CharField(max_length=4096)

    def clean_project_id(self):
        project_id = self.cleaned_data.get('project_id')

        try:
            Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise forms.ValidationError("Projekt nie istnieje")
        return project_id