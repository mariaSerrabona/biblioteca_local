#patrones de la app a mediada que la vamso creado

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]