from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book

#administración de todos los autores con todos sus atributos
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')

    #elemnetos que se van a desplegar en la web
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

#TabularInline diseño horizontal
class BooksInstanceInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance

#administración de todos los libros con sus atributos
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


admin.site.register(Book, BookAdmin)

#adminsitración de la disponibilidad de los libros
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )