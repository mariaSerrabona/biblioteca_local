from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Lenguage

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    #la definimos con los atributos que caracterizan a un autor
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass

#importamos todas las clases que hemos creado antes en el models.py y las de las clases de arriba
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Lenguage)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(BookInstance)