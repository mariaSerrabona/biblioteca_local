import datetime
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import RenewBookForm
from .models import Book, Author, BookInstance
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import login_required, permission_required


#controles de acceso a zonas de la pagina web
from django.contrib.auth.mixins import PermissionRequiredMixin






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
    num_visits=request.session.get('num_visits', 1)
    request.session['num_visits']=num_visits+1

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



#con esta clase podemos ver el número de libros alquilados por cada usuario
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



#con esta clase, tenemos una vista general de todos los libros prestados a todos los usuarios
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})


    #render para crear la página de html
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


#modificar objetos del tipo autor
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial={'date_of_death':'05/01/2018',}
    #marcamos los permisos necesarios para añadir un autor
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

    #marcamos los permisos necesarios para añadir un autor
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    #marcamos los permisos necesarios para añadir un autor
    permission_required = 'catalog.can_mark_returned'
