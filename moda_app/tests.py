from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from moda_app.persistence.models import Product, Category, Inventory
from django.core.exceptions import ValidationError

class CategoryModelTest(TestCase):
    def setUp(self):
        self.categoria = Category.objects.create(name="Accesorios", description="Accesorios eco-friendly")

    def test_crear_categoria(self):
        """Se debe crear la categoría con nombre y descripción"""
        self.assertEqual(self.categoria.name, "Accesorios")
        self.assertEqual(self.categoria.description, "Accesorios eco-friendly")

    def test_nombre_unico(self):
        """Debe fallar si se intenta crear otra categoría con el mismo nombre"""
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Accesorios", description="Duplicado")

    def test_editar_categoria(self):
        """Se debe poder modificar la descripción"""
        self.categoria.description = "Accesorios reciclados"
        self.categoria.save()
        c = Category.objects.get(id=self.categoria.id)
        self.assertEqual(c.description, "Accesorios reciclados")


class ProductModelTest(TestCase):
    def setUp(self):
        self.categoria = Category.objects.create(name="Ropa", description="Categoría de ropa")
        self.producto = Product.objects.create(
            name="Camiseta Eco",
            description="Camiseta sostenible",
            id_categoria=self.categoria,
            disponibilidad=True,
            price=150.00,
            image="http://example.com/camiseta.jpg"
        )

    def test_crear_producto(self):
        """Debe crearse un producto con sus atributos"""
        self.assertEqual(self.producto.name, "Camiseta Eco")
        self.assertTrue(self.producto.disponibilidad)
        self.assertEqual(float(self.producto.price), 150.00)

    def test_actualizar_precio_producto(self):
        """Debe permitir actualizar el precio correctamente"""
        self.producto.price = 180.50
        self.producto.save()
        p = Product.objects.get(id=self.producto.id)
        self.assertEqual(float(p.price), 180.50)

    def test_producto_nombre_unico(self):
        """Debe fallar si se crea un producto con nombre duplicado"""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Camiseta Eco",
                description="Otro producto",
                id_categoria=self.categoria,
                disponibilidad=True,
                price=100.00
            )


class InventoryModelTest(TestCase):
    def setUp(self):
        self.categoria = Category.objects.create(name="Zapatos", description="Calzado sostenible")
        self.producto = Product.objects.create(
            name="Zapatos Verdes",
            description="Zapatos reciclados",
            id_categoria=self.categoria,
            disponibilidad=True,
            price=300.00
        )
        self.inventario = Inventory.objects.create(
            product=self.producto,
            category=self.categoria,
            quantity=20,
            status="Disponible"
        )

    def test_inventario_creacion(self):
        """Inventario debe reflejar cantidad y status"""
        self.assertEqual(self.inventario.quantity, 20)
        self.assertEqual(self.inventario.status, "Disponible")

    def test_inventario_actualizacion_cantidad_a_cero(self):
        """Actualizar cantidad a cero debe cambiar estado a Agotado"""
        self.inventario.quantity = 0
        self.inventario.status = "Agotado"
        self.inventario.save()
        inv = Inventory.objects.get(id=self.inventario.id)
        self.assertEqual(inv.quantity, 0)
        self.assertEqual(inv.status, "Agotado")

def test_cantidad_no_negativa(self):
    self.inventario.quantity = -5
    with self.assertRaises(ValidationError):
        self.inventario.full_clean() 
        self.inventario.save()


class VistaCatalogoTest(TestCase):
    def setUp(self):
        self.categoria = Category.objects.create(name="Bolsos", description="Bolsos sostenibles")
        self.producto = Product.objects.create(
            name="Bolso Eco",
            description="Bolso hecho con materiales reciclados",
            id_categoria=self.categoria,
            disponibilidad=True,
            price=250.00,
            image="http://example.com/bolso.jpg"
        )
        Inventory.objects.create(
            product=self.producto,
            category=self.categoria,
            quantity=8,
            status="Disponible"
        )

    def test_catalogo_home_muestra_productos_y_categorias(self):
        url = reverse('catalogo_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('productos', response.context)
        self.assertIn('categorias', response.context)
        self.assertTrue(any(p.name == "Bolso Eco" for p in response.context['productos']))

    def test_filtrar_por_categoria_retorna_productos_filtrados(self):
        url = reverse('filtrar_por_categoria', args=[self.categoria.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        productos = response.context['productos']
        self.assertTrue(all(p.id_categoria == self.categoria.id for p in productos))

    def test_detalle_producto_existente(self):
        url = reverse('detalle_producto', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.name)
        self.assertContains(response, str(self.producto.price))

    def test_detalle_producto_inexistente_404(self):
        url = reverse('detalle_producto', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

