#patrones de la app a mediada que la vamso creado

from django.urls import path

from . import views


##  ¿QUÉ SIGNIFICAN LOS CARACTERES DE LAS URL?

# ^ inicio de cadena y $  fin de cadena
# ? captura el patron como una variable con nombre
# /d representa un dígito
#r'^book/(?P<pk>\d+)$' camputa todos los dígitos y los envía como una cadena


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
        views.AuthorDetailView.as_view(), name='author-detail'),

]