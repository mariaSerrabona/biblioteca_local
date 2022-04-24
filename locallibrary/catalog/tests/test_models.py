# se genera la carpeta de los test

#cuando se quiere probar una web, cuando es sencilla, es fácil y rápido de probar, pero cunado la web va teniendo mayo número de widgeds, se puede tardar mucho tiempo
#por ello, django nos ofrece la posibilidad de poder porbar nuestra página web para así ver que estaá todo correcto

from django.test import TestCase

# Create your tests here.

class YourTestClass(TestCase):

    #para el comienzo de la ejecución. obj que no se modifican en ningún momento de la prueba.
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    #cualquier obj que oouede ser modificado durante la prueba
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    #assert comprobar si las condiciones son verdaderas o falsas.
    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)