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