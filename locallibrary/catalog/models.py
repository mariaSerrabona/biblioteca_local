from django.db import models

# Create your models here.

class MyModelName(models.Model):
    """
    Una clase típica definiendo un modelo, derivado desde la clase Model.
    """

    # Cadena de caracteres, tiene etiqueta de texto de ayuda (help_txt)
    my_field_name = models.CharField(max_length=20, help_text="Enter field documentation")
    ...

    # Metadata, controla el orden pro defecrto de los registrosque se devuelve cuando se consulta el tipo de modelo.
    #los libros irán ordenados alfabéticamente
    class Meta:
        ordering = ["-my_field_name"]

    # Métodos
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular de MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto MyModelName (en el sitio de Admin, etc.)
        """
        return self.field_name




# Creación de un nuevo registro usando el constructor del modelo.
a_record = MyModelName(my_field_name="Instancia #1")

# Guardar el objeto en la base de datos.
a_record.save()