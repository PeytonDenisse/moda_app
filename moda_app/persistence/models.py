from django.db import models

from django.contrib.auth.models import User





class Category(models.Model):
    # Django ya crea automáticamente el campo 'id'
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'categoria'
        ordering = ['name']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Product(models.Model):
    # Django también crea 'id' automáticamente
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    id_categoria = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='id_categoria')
    disponibilidad = models.BooleanField(default=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'producto_sostenible'
        ordering = ['name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_product_name')
        ]

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=[
        ('Disponible', 'Disponible'),
        ('Agotado', 'Agotado'),
        ('Próximamente', 'Próximamente')
    ])
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventario'
        ordering = ['product']
        verbose_name = 'Inventario del Producto'
        verbose_name_plural = 'Inventario de Productos'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} disponibles"
