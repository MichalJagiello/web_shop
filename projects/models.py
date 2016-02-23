
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from autoryzacja.models import PipesUser

from pipes_types.models import PipeDiameter, PipeColor, PipeType, PipeLeftEnd, PipeRightEnd, PipeMark

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

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projekty'

    def __repr__(self):
        print("Projekt {} użytkownika {}".format(self.name, self.user.email))

    def __str__(self):
        return "Projekt {} użytkownika {}".format(self.name, self.user.email)


class Prefabricate(models.Model):

    project = models.ForeignKey(Project, verbose_name='Projekt')
    pipe_mark = models.ForeignKey(PipeMark, verbose_name='Oznaczenie prefabrykatu')
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

    def __repr__(self):
        print("Prefabrykat {} projektu {} użytkownika".format(self.index, self.project.name, self.project.user.get_full_name()))

    def __str__(self):
        return "Prefabrykat {} projektu {} użytkownika".format(self.index, self.project.name, self.project.user.get_full_name())