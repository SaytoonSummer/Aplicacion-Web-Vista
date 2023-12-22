from django.core.management.base import BaseCommand
from App.models import Producto


class Command(BaseCommand):
    help = 'Elimina todos los productos de la base de datos de Django'

    def handle(self, *args, **kwargs):
        # Eliminar todos los productos
        Producto.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Todos los productos han sido eliminados con éxito'))
