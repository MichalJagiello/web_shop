
from django.conf.urls import url

from web.views import MainPageView,\
                      FirstStepView,\
                      SecondStepView,\
                      ThirdStepView,\
                      FourthStepView, \
                      RegistrationView,\
                      SaveProjectView, \
                      FinishProjectView, \
                      RegistrationFormView,\
                      ThanksView, \
                      NextPrefabricateView, \
                      DeletePrefabricateView, \
                      EditPrefabricateView, \
                      MultiplyPrefabricateView, \
                      ColorFilterView, \
                      OutflowsManipulateView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'krok_1/$', FirstStepView.as_view(), name='krok_1'),
    url(r'krok_2/$', SecondStepView.as_view(), name='krok_2'),
    url(r'krok_3/$', ThirdStepView.as_view(), name='krok_3'),
    url(r'krok_4/$', FourthStepView.as_view(), name='krok_4'),
    url(r'next_prefabricate/$', NextPrefabricateView.as_view(), name='nastepny_prefabrykat'),
    url(r'usun_prefabrykat/(?P<prefabricate_index>\d+)/$', DeletePrefabricateView.as_view(), name='usun_prefabrykat'),
    url(r'edytuj_prefabrykat/(?P<prefabricate_index>\d+)/$', EditPrefabricateView.as_view(), name='edytuj_prefabrykat'),
    url(r'powiel_prefabrykat/(?P<prefabricate_index>\d+)/$', MultiplyPrefabricateView.as_view(), name='powiel_prefabrykat'),
    url(r'zapisz_projekt/$', SaveProjectView.as_view(), name='zapisz_projekt'),
    url(r'zakoncz_projekt/$', FinishProjectView.as_view(), name='zakoncz_projekt'),
    url(r'register/$', RegistrationFormView.as_view(), name='registration'),
    url(r'thanks/$', ThanksView.as_view(), name='registation_thanks'),

    url(r'^krok_2/filter_colors/$', ColorFilterView.as_view(), name='filter_colors'),
    url(r'^krok_3/outflow/$', OutflowsManipulateView.as_view(), name='outflows_manipulate'),
]
