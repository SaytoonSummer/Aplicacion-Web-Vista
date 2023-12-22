from django.db import models


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    ventas = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre_producto

    class Meta:
        db_table = 'Producto'


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre_proveedor

    class Meta:
        db_table = 'Proveedor'
