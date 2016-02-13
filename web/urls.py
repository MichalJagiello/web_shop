
from django.conf.urls import url

from web.views import MainPageView, FirstStepView, SecondStepView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'krok_1/$', FirstStepView.as_view(), name='krok_1'),
    url(r'krok_2/$', SecondStepView.as_view(), name='krok_2'),
]
