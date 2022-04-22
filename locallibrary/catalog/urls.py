#patrones de la app a mediada que la vamso creado

from django.conf.urls import url

from . import views


##  ¿QUÉ SIGNIFICAN LOS CARACTERES DE LAS URL?

# ^ inicio de cadena y $  fin de cadena
# ? captura el patron como una variable con nombre
# /d representa un dígito
#r'^book/(?P<pk>\d+)$' camputa todos los dígitos y los envía como una cadena


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'author/<int:pk>$',
        views.AuthorDetailView.as_view(), name='author-detail'),

]