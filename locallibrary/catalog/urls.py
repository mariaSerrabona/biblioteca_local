#patrones de la app a mediada que la vamso creado

from django.conf.urls import url

from . import views


# ^ inicio de cadena y $  fin de cadena

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
]