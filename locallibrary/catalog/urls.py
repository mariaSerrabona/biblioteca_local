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
    path('authors/<int:pk>',
        views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),

    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

]


#url con lo referente a la edición de autores
urlpatterns += [
    path('authors/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

#url con lo referente a la edición de libros
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

