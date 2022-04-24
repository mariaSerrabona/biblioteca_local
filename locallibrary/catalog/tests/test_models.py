# se genera la carpeta de los test

#cuando se quiere probar una web, cuando es sencilla, es fácil y rápido de probar, pero cunado la web va teniendo mayo número de widgeds, se puede tardar mucho tiempo
#por ello, django nos ofrece la posibilidad de poder porbar nuestra página web para así ver que estaá todo correcto

from django.test import TestCase
from catalog.models import Author


#hacemos las pruebas para ver si la parte de los autores etsá bien
class AuthorModelTest(TestCase):

    #se genera un test por cada objeto que define un autor
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        #no podemos acceder directamente a los datos del autor, primero debemos acceder a su clase meta y usuarla para obtener info adicional
        field_label = author._meta.get_field('first_name').verbose_name
        #se emplea esta estructura para que el error salte exactamente donde está, haciendo más fácil el debugging
        self.assertEquals(field_label,'first name')


    def test_last_name_label(self):
        author=Author.objects.get(id=1)
        #no podemos acceder directamente a los datos del autor, primero debemos acceder a su clase meta y usuarla para obtener info adicional
        field_label = author._meta.get_field('last_name').verbose_name
        #se emplea esta estructura para que el error salte exactamente donde está, haciendo más fácil el debugging
        self.assertEquals(field_label,'last name')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    #completando las pruebas con otros campos de los autores
    def test_last_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length,100)

    #siguiendo con los test, habrá que comprobar la fecha de nacimiento
    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #También fallará si la url no está bien configurada
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')