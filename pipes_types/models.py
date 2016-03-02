#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class PipeDiameter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Rodzaj średnicy')
    available = models.BooleanField(default=True, verbose_name='Dostępny')
    size = models.CharField(max_length=16, verbose_name='Rozmiar')

    class Meta:
        verbose_name = 'Średnica rury'
        verbose_name_plural = 'Średnice rur'

    def __str__(self):
        return "{} ({})".format(self.name, self.size)


class PipeType(models.Model):
    name = models.CharField(max_length=16, verbose_name='Typ rury')
    available = models.BooleanField(default=True, verbose_name='Dostępny')
    color_allowed = models.BooleanField(default=True, verbose_name='Dostępny z kolorem')


    class Meta:
        verbose_name = 'Typ rury'
        verbose_name_plural = 'Typy rur'

    def __str__(self):
        return self.name


class PipeColor(models.Model):
    name = models.CharField(max_length=32, verbose_name='Nazwa koloru')
    available = models.BooleanField(default=True, verbose_name='Dostępny')

    class Meta:
        verbose_name = 'Kolor rury'
        verbose_name_plural = 'Kolory rur'

    def __str__(self):
        return self.name


class PipeMark(models.Model):
    name = models.CharField(max_length=16, verbose_name='Oznaczenie rury', unique=True)
    available = models.BooleanField(default=True, verbose_name='Dostępny')

    class Meta:
        verbose_name = 'Oznaczenie rury'
        verbose_name_plural = 'Oznaczenia rur'

    def __str__(self):
        return self.name


class PipeLeftEnd(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa zakończenia', unique=True)
    image = models.ImageField(verbose_name='Obrazek zakończenia', upload_to='zakonczenia_lewe')
    available = models.BooleanField(default=True, verbose_name='Dostępne')
    pipe_image = models.ImageField(verbose_name='Obrazek zakończenia z rurą', upload_to='zakonczenia_lewe')

    class Meta:
        verbose_name = 'Zakończenie rury lewe'
        verbose_name_plural = 'Zakończenia rur lewe'

    def __str__(self):
        return self.name


class PipeRightEnd(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa zakończenia', unique=True)
    image = models.ImageField(verbose_name='Obrazek zakończenia', upload_to='zakonczenia_prawe')
    available = models.BooleanField(default=True, verbose_name='Dostępne')
    pipe_image = models.ImageField(verbose_name='Obrazek zakończenia z rurą', upload_to='zakonczenia_prawe')

    class Meta:
        verbose_name = 'Zakończenie rury prawe'
        verbose_name_plural = 'Zakończenia rur prawe'

    def __str__(self):
        return self.name


class PipeOutflow(models.Model):
    pass