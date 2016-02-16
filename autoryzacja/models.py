#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager, BaseUserManager
from django.db import models

# Create your models here.

class PipesUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        """
        Create and save user object
        """
        if not email:
            raise ValueError("Użytkownik musi posiadać adres email")

        if not password:
            raise ValueError("Użytkownik musi posiadać hasło")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Użytkownik musi posiadać adres email")

        if not password:
            raise ValueError("Użytkownik musi posiadać hasło")

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user

class PipesUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Adres email',
                              unique=True,
                              max_length=255)

    first_name = models.CharField(max_length=32,
                                  null=False,
                                  verbose_name='Imię')
    last_name = models.CharField(max_length=64,
                                 null=False,
                                 verbose_name='Nazwisko')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = PipesUserManager()

    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, package_name):
        print(package_name)
        if package_name == 'auth':
            if self.is_staff:
                return True
            return False
        return self.is_staff

    @property
    def is_staff(self):
        return self.is_admin