from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.

    # queremos saber el número de visitas que ah recibido muestra página web
    num_visits= request.session['num_visits']
    num_visits+=1

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
    }

    #se conecta con la plantilla html que hemos creado en templates

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )


class BookListView(generic.ListView):
    model = Book

    #paginación para que el servidor no trade tanto en cargar los libros
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


## retate a ti mismo: creand las views de los detalles de los autores
class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    #lo paginamos para que el servidor no tarde  nucho en cargar
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author