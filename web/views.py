#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from autoryzacja.forms import RegisterForm
from autoryzacja.models import PipesUser

from projects.forms import NewProjectForm, EditProjectForm, AddPrefabricateForm, OutflowManipulateFormAdd, OutflowManipulateFormDelete, OutflowDistanceManipulateForm
from projects.models import Project, Prefabricate, PrefabricateOutflow

from pipes_types.forms import UpdateColorSelectForm
from pipes_types.models import PipeType, PipeOutflow

import pdf_generator

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
    edit_form_class = EditProjectForm
    template = 'krok_1.html'

    def get(self, request):
        session_project = request.session.get('project', None)
        if session_project is not None:
            try:
                project = Project.objects.get(id=session_project)
            except Project.DoesNotExist:
                form = self.form_class()
                del request.session['project']
                if request.session.has_key('prefabricate_index'):
                    del request.session['prefabricate_index']
                if request.session.has_key('prefabricate'):
                    del request.session['prefabricate']
            else:
                form = self.form_class(initial={
                    'city': project.city,
                    'name': project.name,
                    'number': project.number,
                    'postcode': project.postcode,
                    'street': project.street,
                })
        else:
            form = self.form_class()
        return render(request, self.template, {'user_full_name': request.user.get_full_name(),
                                               'form': form})

    def post(self, request):

        session_project = request.session.get('project', None)
        if session_project is None:
            form = self.form_class(request.POST)
        else:
            form = self.edit_form_class(request.POST)

        if form.is_valid():

            if session_project is not None:
                project = Project.objects.get(id=session_project)
                project.name = form.cleaned_data.get('name')
                project.city = form.cleaned_data.get('city')
                project.street = form.cleaned_data.get('street')
                project.postcode = form.cleaned_data.get('postcode')
                project.number = form.cleaned_data.get('number')

                project.save()

            else:
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
    template = 'krok_2.html'
    form_class = AddPrefabricateForm

    def get(self, request):
        session_prefabricate = request.session.get('prefabricate', None)

        if session_prefabricate:
            try:
                prefabricate = Prefabricate.objects.get(id=session_prefabricate)
            except Prefabricate.DoesNotExist:
                del request.session['prefabricate']
                form = self.form_class()
            else:
                form = self.form_class(initial={'diameter': prefabricate.pipe_diameter,
                                                'type': prefabricate.pipe_type,
                                                'mark': prefabricate.prefabricate_mark,
                                                'color': prefabricate.pipe_color,
                                                'left_end': prefabricate.pipe_left_end,
                                                'right_end': prefabricate.pipe_right_end,
                                                'quantity': prefabricate.count})
        else:
            form = self.form_class()
        return render(request, self.template, {'user_full_name': request.user.get_full_name(),
                                               'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            session_prefabricate = request.session.get('prefabricate', None)

            if session_prefabricate:
                prefabricate = Prefabricate.objects.get(id=session_prefabricate)
                prefabricate.pipe_diameter = form.cleaned_data.get('diameter')
                prefabricate.pipe_type = form.cleaned_data.get('type')
                prefabricate.prefabricate_mark = form.cleaned_data.get('mark')
                prefabricate.pipe_color = form.cleaned_data.get('color')
                prefabricate.pipe_left_end = form.cleaned_data.get('left_end')
                prefabricate.pipe_right_end = form.cleaned_data.get('right_end')
                prefabricate.count = form.cleaned_data.get('quantity')
                prefabricate.save()
            else:
                project = Project.objects.get(id=request.session.get('project'))
                prefabricate_index = request.session.get('prefabricate_index', 0)
                prefabricate = Prefabricate.objects.create(project=project,
                                                           pipe_diameter=form.cleaned_data.get('diameter'),
                                                           pipe_type=form.cleaned_data.get('type'),
                                                           prefabricate_mark=form.cleaned_data.get('mark'),
                                                           pipe_color=form.cleaned_data.get('color'),
                                                           pipe_left_end=form.cleaned_data.get('left_end'),
                                                           pipe_right_end=form.cleaned_data.get('right_end'),
                                                           count=form.cleaned_data.get('quantity'),
                                                           index=prefabricate_index)
                request.session['prefabricate'] = prefabricate.id

            return redirect('krok_3')

        return render(request, self.template, {'user_full_name': request.user.get_full_name(),
                                               'form': form})


class ThirdStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        prefabricate = Prefabricate.objects.get(id=request.session.get('prefabricate'))
        outflows = PipeOutflow.objects.filter(available=True)
        prefabricate_outflows = PrefabricateOutflow.objects.filter(prefabricate=prefabricate)
        return render(request, 'krok_3.html', {'user_full_name': request.user.get_full_name(),
                                               'prefabricate': prefabricate,
                                               'outflows': outflows,
                                               'prefabricate_outflows': prefabricate_outflows})


class ThirdAndHalfStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        prefabricate_id = request.session.get('prefabricate', None)
        if prefabricate_id is None:
            raise Http404("Project is saved")
        prefabricate = Prefabricate.objects.get(id=request.session.get('prefabricate'))
        prefabricate_outflows = PrefabricateOutflow.objects.filter(prefabricate=prefabricate)
        return render(request, 'krok_3_5.html', {'user_full_name': request.user.get_full_name(),
                                               'prefabricate': prefabricate,
                                               'prefabricate_outflows': prefabricate_outflows})


class FourthStepView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        prefabricate_id = request.session.get('prefabricate', None)
        if prefabricate_id is None:
            raise Http404("Project is saved")
        prefabricate = Prefabricate.objects.get(id=request.session.get('prefabricate'))
        prefabricate_outflows = PrefabricateOutflow.objects.filter(prefabricate=prefabricate)
        return render(request, 'krok_4.html', {'user_full_name': request.user.get_full_name(),
                                               'prefabricate': prefabricate,
                                               'prefabricate_outflows': prefabricate_outflows})

class NextPrefabricateView(LoginRequiredMixin, View):

    def get(self, request):
        project = Project.objects.get(id=request.session.get('project'))
        request.session['prefabricate_index'] = len(Prefabricate.objects.filter(project=project))
        request.session['prefabricate'] = None
        return redirect('krok_2')


class DeletePrefabricateView(LoginRequiredMixin, View):

    def get(self, request, prefabricate_index):
        project = Project.objects.get(id=request.session.get('project'))
        prefabricate = Prefabricate.objects.get(project=project, index=prefabricate_index)
        for prefabricate_outflow in PrefabricateOutflow.objects.filter(prefabricate=prefabricate):
            prefabricate_outflow.delete()
        prefabricate.delete()
        for prefabricate in Prefabricate.objects.filter(project=project, index__gt=prefabricate_index):
            prefabricate.index = prefabricate.index - 1
            prefabricate.save()
        return redirect('zapisz_projekt')

class MultiplyPrefabricateView(LoginRequiredMixin, View):

    def get(self, request, prefabricate_index):
        project = Project.objects.get(id=request.session.get('project'))
        prefabricate = Prefabricate.objects.get(project=project, index=prefabricate_index)
        prefabricate_copy = Prefabricate.objects.create(project=project,
                                                        pipe_diameter=prefabricate.pipe_diameter,
                                                        pipe_type=prefabricate.pipe_type,
                                                        prefabricate_mark=prefabricate.prefabricate_mark,
                                                        pipe_color=prefabricate.pipe_color,
                                                        pipe_left_end=prefabricate.pipe_left_end,
                                                        pipe_right_end=prefabricate.pipe_right_end,
                                                        count=prefabricate.count,
                                                        index=len(Prefabricate.objects.filter(project=project)))
        for prefabricate_outflow in PrefabricateOutflow.objects.filter(prefabricate=prefabricate):
            PrefabricateOutflow.objects.create(prefabricate=prefabricate_copy,
                                               outflow=prefabricate_outflow.outflow,
                                               index=prefabricate_outflow.index,
                                               distance=prefabricate_outflow.distance)
        return redirect('zapisz_projekt')

class EditPrefabricateView(LoginRequiredMixin, View):

    def get(self, request, prefabricate_index):
        project = Project.objects.get(id=request.session.get('project'))
        prefabricate = Prefabricate.objects.get(project=project, index=prefabricate_index)
        request.session['prefabricate_index'] = prefabricate_index
        request.session['prefabricate'] = prefabricate.id
        return redirect('krok_2')


class SaveProjectView(LoginRequiredMixin, View):

    def get(self, request):
        project_obj = Project.objects.get(id=request.session.get('project'))

        prefabricates = Prefabricate.objects.filter(project=project_obj).order_by('index')

        return render(request, 'krok_5.html', {'user_full_name': request.user.get_full_name(),
                                               'prefabricates': prefabricates})


class FinishProjectView(LoginRequiredMixin, View):

    def get(self, request):

        project = Project.objects.get(id=request.session.get('project'))
        prefabricates = Prefabricate.objects.filter(project=project).order_by('index')
        prefabricates_outflows = PrefabricateOutflow.objects.filter(prefabricate__in=prefabricates)

        template = render_to_string('pdf_template.html', {'user_full_name': request.user.get_full_name(),
                                                                  'project': project,
                                                                  'prefabricates': prefabricates,
                                                                  'prefabricate_outflows': prefabricates_outflows,
                                                                  'rura_lewa_image': os.path.join(settings.BASE_DIR, 'static/img/rura.png'),
                                                                  'rura_lewa_rowek_image': os.path.join(settings.BASE_DIR, 'static/img/rura_rowek_lewa.png'),
                                                                  'rura_lewa_owal_image': os.path.join(settings.BASE_DIR, 'static/img/rura_owal_lewa.png'),
                                                                  'rura_prawa_image': os.path.join(settings.BASE_DIR, 'static/img/rura.png'),
                                                                  'rura_prawa_owal_image': os.path.join(settings.BASE_DIR, 'static/img/rura_owal_prawa.png'),
                                                                  'rura_prawa_rowek_image': os.path.join(settings.BASE_DIR, 'static/img/rura_rowek_prawa.png'),
                                                                  'odejscie_tyl_image': os.path.join(settings.BASE_DIR, 'static/img/tyl.png'),
                                                                  'odejscie_przod_image': os.path.join(settings.BASE_DIR, 'static/img/przod.png'),
                                                                  'odejscie_dol_image': os.path.join(settings.BASE_DIR, 'static/img/dol.png'),
                                                                  'odejscie_gora_image': os.path.join(settings.BASE_DIR, 'static/img/gora.png'),
                                                                  'strzalka_image': os.path.join(settings.BASE_DIR, 'static/img/strzalka_l.jpg'),
                                                                  'logo_image': os.path.join(settings.BASE_DIR, 'static/img/logo.png')})

        email = EmailMessage('Nowy projekt', 'Nowy projekt stworzony przez klienta', 'dekk@pipesprefabrication.pl', ['michal.jgl@gmail.com', 'info@dekk.pl', 'kontakt@strony-piaseczno.pl'])
        email.attach('projekt.pdf', pdf_generator.generate(template), 'application/pdf')
        email.send()

        if request.session.has_key('project'):
            project = request.session.get('project')
            project_obj = Project.objects.get(id=project)
            project_obj.saved = True
            project_obj.pdf.save('.'.join([project_obj.name, 'pdf']), ContentFile(pdf_generator.generate(project_obj.name)))
            project_obj.save()
        if request.session.has_key('prefabricate_index'):
            del request.session['prefabricate_index']
        if request.session.has_key('prefabricate'):
            del request.session['prefabricate']
        if request.session.has_key('project'):
            del request.session['project']

        return render(request, 'project_created.html', {'user_full_name': request.user.get_full_name()})


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


class ColorFilterView(View):

    form_class = UpdateColorSelectForm

    def get(self, request):
        form_class = UpdateColorSelectForm(request.GET)

        if not form_class.is_valid():
            raise SuspiciousOperation("Invalid form")

        pipe_type_id = form_class.cleaned_data.get('type_id')
        if pipe_type_id is None:
            return JsonResponse({'error': False,
                                 'color_enabled': True})

        pipe_type = get_object_or_404(PipeType, id=pipe_type_id)
        return JsonResponse({'error': False,
                             'color_enabled': pipe_type.color_allowed})


class OutflowsManipulateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OutflowsManipulateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        form = OutflowManipulateFormAdd(request.GET)

        if not form.is_valid():
            print(form.errors)
            raise SuspiciousOperation("Invalid form")

        prefabricate = Prefabricate.objects.get(id=form.cleaned_data.get('prefabricate_id'))
        outflow = PipeOutflow.objects.get(id=form.cleaned_data.get('outflow_id'))
        index = form.cleaned_data.get('index')

        try:
            pref_outflow = PrefabricateOutflow.objects.get(prefabricate=prefabricate,
                                                           index=index)
            pref_outflow.outflow = outflow
            pref_outflow.distance = 1
            pref_outflow.save()
        except PrefabricateOutflow.DoesNotExist:
            PrefabricateOutflow.objects.create(prefabricate=prefabricate,
                                               outflow=outflow,
                                               index=index,
                                               distance=1)

        return HttpResponse()

    def delete(self, request):
        form = OutflowManipulateFormDelete(request.GET)

        if not form.is_valid():
            raise SuspiciousOperation("Invalid form")

        prefabricate = Prefabricate.objects.get(id=form.cleaned_data.get('prefabricate_id'))
        index = form.cleaned_data.get('index')

        try:
            PrefabricateOutflow.objects.get(prefabricate=prefabricate,
                                            index=index).delete()
        except PrefabricateOutflow.DoesNotExist:
            raise SuspiciousOperation("Outflow not exists")

        return HttpResponse()


class OutflowDistanceManipulateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OutflowDistanceManipulateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        form = OutflowDistanceManipulateForm(request.GET)

        if not form.is_valid():
            print(form.errors)
            raise SuspiciousOperation("Invalid form")

        prefabricate = Prefabricate.objects.get(id=form.cleaned_data.get('prefabricate_id'))
        index = form.cleaned_data.get('index')

        try:
            prefabricate_outflow = PrefabricateOutflow.objects.get(prefabricate=prefabricate,
                                            index=index)
        except PrefabricateOutflow.DoesNotExist:
            raise SuspiciousOperation("Outflow not exists")

        print(form.cleaned_data)

        prefabricate_outflow.distance = form.cleaned_data.get('distance')
        prefabricate_outflow.save()

        return HttpResponse()

class PrintPdfFileView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):

        project = Project.objects.get(id=request.session.get('project'))
        prefabricates = Prefabricate.objects.filter(project=project).order_by('index')
        prefabricates_outflows = PrefabricateOutflow.objects.filter(prefabricate__in=prefabricates)

        template = render_to_string('pdf_template.html', {'user_full_name': request.user.get_full_name(),
                                                                  'project': project,
                                                                  'prefabricates': prefabricates,
                                                                  'prefabricate_outflows': prefabricates_outflows,
                                                                  'rura_lewa_image': os.path.join(settings.BASE_DIR, 'static/img/rura.png'),
                                                                  'rura_lewa_rowek_image': os.path.join(settings.BASE_DIR, 'static/img/rura_rowek_lewa.png'),
                                                                  'rura_lewa_owal_image': os.path.join(settings.BASE_DIR, 'static/img/rura_owal_lewa.png'),
                                                                  'rura_prawa_image': os.path.join(settings.BASE_DIR, 'static/img/rura.png'),
                                                                  'rura_prawa_owal_image': os.path.join(settings.BASE_DIR, 'static/img/rura_owal_prawa.png'),
                                                                  'rura_prawa_rowek_image': os.path.join(settings.BASE_DIR, 'static/img/rura_rowek_prawa.png'),
                                                                  'odejscie_tyl_image': os.path.join(settings.BASE_DIR, 'static/img/tyl.png'),
                                                                  'odejscie_przod_image': os.path.join(settings.BASE_DIR, 'static/img/przod.png'),
                                                                  'odejscie_dol_image': os.path.join(settings.BASE_DIR, 'static/img/dol.png'),
                                                                  'odejscie_gora_image': os.path.join(settings.BASE_DIR, 'static/img/gora.png'),
                                                                  'strzalka_image': os.path.join(settings.BASE_DIR, 'static/img/strzalka_l.jpg'),
                                                                  'logo_image': os.path.join(settings.BASE_DIR, 'static/img/logo.png')})

        return HttpResponse(pdf_generator.generate(template), 'application/pdf')