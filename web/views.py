from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.

class MainPageView(View):
    def get(self, request):
        return render(request, 'main.html')


class FirstStepView(View):
    def get(self, request):
        return render(request, 'krok_1.html')


class SecondStepView(View):
    def get(self, request):
        return render(request, 'krok_2.html')