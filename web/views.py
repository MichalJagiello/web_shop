#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from autoryzacja.forms import LoginForm, RegisterForm
from autoryzacja.models import PipesUser

from projects.forms import NewProjectForm
from projects.models import Project

# Create your views here.

class MainPageView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'main.html', {'authenticated': request.user.is_authenticated(),
                                                 'user_full_name': request.user.get_full_name()})
        return render(request, 'main.html', {'authenticated': request.user.is_authenticated(),
                                             'user_full_name': ''})


class FirstStepView(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = NewProjectForm
    template = 'krok_1.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'user_full_name': request.user.get_full_name(),
                                               'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            project = Project.objects.create(user = request.user,
                                             name = form.cleaned_data.get('name'),
                                             city=form.cleaned_data.get('city'),
                                             street=form.cleaned_data.get('street'),
                                             postcode=form.cleaned_data.get('postcode'),
                                             number=form.cleaned_data.get('number'))

            request.session['project'] = project.id

            return redirect('krok_2')

        return render(request, self.template, {'user_full_name': request.user.get_full_name(),
                                               'form': form})



class SecondStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'krok_2.html', {'user_full_name': request.user.get_full_name()})


class ThirdStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'krok_3.html', {'user_full_name': request.user.get_full_name()})


class FourthStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'krok_4.html', {'user_full_name': request.user.get_full_name()})


class RegistrationView(View):

    def get(self, request):
        return render(request, 'register.html', {'form': RegisterForm()})

    def post(self, request):
        pass


class RegistrationFormView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = 'registation_thanks'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = PipesUser(email=form.cleaned_data['email'],
                         first_name=form.cleaned_data['first_name'],
                         last_name=form.cleaned_data['last_name'])
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super(RegistrationFormView, self).form_valid(form)


class ThanksView(View):

    def get(self, request):
        return render(request, 'thanks.html')