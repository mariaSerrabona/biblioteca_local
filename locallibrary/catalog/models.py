from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm
from django.core.exceptions import ValidationError




# Create your models here.

class Language (models.Model):

    #atributos que definen a un lenguaje: el nombre del idioma
    #lo dotamos como un CharField puesto que se introducirán caracteres alfanuméticos
    name=models.CharField(max_length=150, help_text='Introduzca el idioma en el que está escrito el libro (Castellano, Inglés, Portugués...)')

    #ahora falta llamar al método que nos devuelva el idioma:

    def __str__(self):
        return self.name


#segunda clase: Genre, clasificación de libros por el género literario
class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.name


#segunda clase:libro (en general), con todos los atributos que caracterizan a un libro
class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.

    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.title


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


#tercera clase: copia específica de uno de los libros que puede ser prerstado pro la biblioteca
class BookInstance(models.Model):


    #se definen las características
    #UUIDField e establece ID como el campo ppal de representación de un libro
        # solo existe un único valor para cada ubno de los libros

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)      #fecha en la que se prevee que vuelva a estar disponible

    #añadimos el usuario que ha tomado prestado el llibro
    borrower=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #aviso para saber si esta atrasado en la fecha de entrega
    @property
    def is_overdue(self):
        if self.due_back and datetime.date.today() > self.due_back:
            return True
        return False


    #estado de libro
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)



    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.book.title)




#cuarta clase: autor
class Author(models.Model):

    #se definen los atributos que caracterizan a un autor
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)

    #ordenar los autores empleando la clase meta
    class Meta:
        ordering = ['last_name']



class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

    #Comprobar que la fecha no es anterior al dia de hoy
        if data < datetime.date.today():
            raise ValidationError(('Invalid date - renewal in past'))

    #Comporbar que la fecha no supera las cuatro semanas a partir de hoy.
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(('Invalid date - renewal more than 4 weeks ahead'))

    # Devolver la fecha.
        return data
    class Meta:
        model = BookInstance
        fields = ['due_back',]
        help_texts = { 'due_back': ('Introduzca una fecha de hoy a 4 semanas (por defecto se derán 3 semanas).'),}




