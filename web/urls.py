
from django.conf.urls import url

from web.views import MainPageView, FirstStepView, SecondStepView, RegistrationView, RegistrationFormView, ThanksView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'krok_1/$', FirstStepView.as_view(), name='krok_1'),
    url(r'krok_2/$', SecondStepView.as_view(), name='krok_2'),
    url(r'register/$', RegistrationFormView.as_view(), name='registration'),
    url(r'thanks/$', ThanksView.as_view(), name='registation_thanks'),
]
