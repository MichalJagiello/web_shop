#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from django import forms
from django.conf import settings
from django.contrib import admin

from autoryzacja.models import PipesUser

from .models import Project, Prefabricate

# Register your models here.

class ProjectCreationForm(forms.ModelForm):

    name = forms.CharField(max_length=255, label='Nazwa projektu')
    user = forms.ModelChoiceField(queryset=PipesUser.objects.all())
    city = forms.CharField(max_length=128, label='Miasto')
    street = forms.CharField(max_length=128, label='Ulica')
    postcode = forms.CharField(max_length=6, label='Kod pocztowy')
    number = forms.CharField(max_length=24, label='Numer')

    class Meta:
        model = Project
        fields = ('name', 'user', 'street', 'number', 'postcode', 'city')

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

    def save(self, commit=True):
        project = super(ProjectCreationForm, self).save(commit=False)
        project.saved = True
        if commit:
            project.save()
        return project


class PrefabricateAdminInline(admin.TabularInline):

    model = Prefabricate
    fields = ('project', 'pipe_mark', 'pipe_diameter', 'pipe_color', 'pipe_type')
    ordering = ('project', 'index')
    can_delete = False
    readonly_fields = ('project', 'pipe_mark', 'pipe_diameter', 'pipe_color', 'pipe_type')

    def get_max_num(self, request, obj=None, **kwargs):

        return len(Prefabricate.objects.filter(project=obj))


class ProjectsAdmin(admin.ModelAdmin):

    model = Project
    list_display = ('name', 'user', 'created', 'edited')
    search_fields = ('name', 'user')
    fieldsets = (
        ('Nazwa', {
            'fields': ('name',),
        }),
        ('Użytkownik', {
            'fields': ('user',),
        }),
        ('Adres', {
            'fields': ('street', 'number', 'postcode', 'city')
        }),
        ('Plik', {
            'fields': ('pdf',)
        }),
    )
    inlines = [
        PrefabricateAdminInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.saved = True
        obj.save()


admin.site.register(Project, ProjectsAdmin)
