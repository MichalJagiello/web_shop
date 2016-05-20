#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from autoryzacja.models import PipesUser

from pipes_types.models import PipeDiameter, PipeColor, PipeType, PipeLeftEnd, PipeRightEnd, PipeMark, PipeOutflow, PipeOutflowSize

# Create your models here.


class Project(models.Model):

    user = models.ForeignKey(PipesUser, verbose_name='Użytkownik')
    name = models.CharField(max_length=255, unique=True, verbose_name='Nazwa projektu')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    edited = models.DateTimeField(auto_now=True, verbose_name='Data ostatniej edycji')
    saved = models.BooleanField(default=False)
    city = models.CharField(max_length=128, verbose_name='Miasto')
    street = models.CharField(max_length=128, verbose_name='Ulica')
    postcode = models.CharField(max_length=6, verbose_name='Kod pocztowy',
                                validators=[RegexValidator(regex=settings.POSTCODE_PATTERN,
                                                           message="Podaj kod pocztowy we właściwym"
                                                                   "formacie, np. 00-000")])
    number = models.CharField(max_length=24, verbose_name='Numer')
    pdf = models.FileField(verbose_name='Plik projektu', null=True, upload_to='projects_files')
    comment = models.TextField(verbose_name='Komentarz do projektu', default='')

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekty'

    #def __repr__(self):
    #    print("Projekt {} użytkownika {}".format(self.name, self.user.email))

    def __str__(self):
        return "Projekt {} użytkownika {}".format(self.name, self.user.email)


class Prefabricate(models.Model):

    project = models.ForeignKey(Project, verbose_name='Projekt')
    prefabricate_mark = models.CharField(max_length=256)
    pipe_diameter = models.ForeignKey(PipeDiameter, verbose_name='Średnica')
    pipe_color = models.ForeignKey(PipeColor, verbose_name='Kolor', null=True)
    pipe_type = models.ForeignKey(PipeType, verbose_name='Rodzaj rury')
    pipe_left_end = models.ForeignKey(PipeLeftEnd, verbose_name='Zakończenie lewe')
    pipe_right_end = models.ForeignKey(PipeRightEnd, verbose_name='Zakończenie prawe')
    index = models.IntegerField(verbose_name='Indeks prefabrykatu w projekcie')
    count = models.IntegerField(verbose_name='Ilość perfabrykatu')

    class Meta:
        verbose_name = 'Prefabrykat'
        verbose_name_plural = 'Prefabrykaty'

    #def __repr__(self):
    #    print("Prefabrykat {} projektu {} użytkownika".format(self.index + 1, self.project.name, self.project.user.get_full_name()))

    def __str__(self):
        return "Prefabrykat {} projektu {} użytkownika".format(self.index + 1, self.project.name, self.project.user.get_full_name())

    @property
    def outflows(self):
        return PrefabricateOutflow.objects.filter(prefabricate=self).order_by('index')

    @property
    def localizations(self):
        localizations = []

        for _ in range(21):
            localizations.append({'outflow': None, 'distance': None, 'first': False, 'last': False})

        for outflow in self.outflows:
            if outflow.first:
                localizations[outflow.index]['outflow'] = outflow
                localizations[outflow.index_between_previous]['distance'] = outflow.distance
                localizations[outflow.index]['first'] = True
            elif outflow.last:
                localizations[outflow.index]['outflow'] = outflow
                localizations[outflow.index_between_end]['distance'] = outflow.distance_to_end
                localizations[outflow.index_between_previous]['distance'] = outflow.distance
                localizations[outflow.index]['last'] = True
            else:
                localizations[outflow.index]['outflow'] = outflow
                localizations[outflow.index_between_previous]['distance'] = outflow.distance

        return localizations


class PrefabricateOutflow(models.Model):

    prefabricate = models.ForeignKey(Prefabricate, verbose_name='Prefabrykat')
    outflow = models.ForeignKey(PipeOutflow, verbose_name='Odejście')
    size = models.ForeignKey(PipeOutflowSize, verbose_name='Rozmiar odejścia')
    index = models.IntegerField(verbose_name='Indeks')
    distance = models.IntegerField(verbose_name='Odległość')
    distance_to_end = models.IntegerField(verbose_name='Odległość do końca', default=10)

    @property
    def index_between_previous(self):
        try:
            prev = PrefabricateOutflow.objects.filter(prefabricate=self.prefabricate, index__lt=self.index).order_by('-index')[0]

            return math.ceil((self.index + prev.index) / 2)
        except IndexError:
            return math.floor(self.index / 2)

    @property
    def index_between_end(self):
        return self.index + math.floor((21 - self.index) / 2)

    @property
    def first(self):
        return self == PrefabricateOutflow.objects.filter(prefabricate=self.prefabricate).order_by('index')[0]

    @property
    def last(self):
        return self == PrefabricateOutflow.objects.filter(prefabricate=self.prefabricate).order_by('-index')[0]