from django.shortcuts import render, get_object_or_404
from moda_app.service.inventario_service import InventoryService
from moda_app.service.product_service import ProductService
from moda_app.service.category_service import CategoryService

# Servicios
producto_service = ProductService()
categoria_service = CategoryService()
inventario_service = InventoryService()

"""
    Vista pública
    Muestra todos los productos y las categorías
"""
def catalogo_home(request):
    productos = producto_service.get_all()
    categorias = categoria_service.get_all()
    inventarios = inventario_service.get_all()

    # Diccionario: producto_id -> cantidad
    cantidad_por_producto = {inv.product_id: inv.quantity for inv in inventarios}

    # Agregar atributo .cantidad a cada producto
    for producto in productos:
        producto.cantidad = cantidad_por_producto.get(producto.id, 0)

    return render(request, 'public/catalogo_home.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': None
    })


def filtrar_por_categoria(request, id):
    productos = [p for p in producto_service.get_all() if p.id_categoria == id]
    categorias = categoria_service.get_all()
    inventarios = inventario_service.get_all()

    # Diccionario: producto_id -> cantidad
    cantidad_por_producto = {inv.product_id: inv.quantity for inv in inventarios}

    # Agregar atributo .cantidad a cada producto
    for producto in productos:
        producto.cantidad = cantidad_por_producto.get(producto.id, 0)

    categoria_actual = next((c for c in categorias if c.id == id), None)

    return render(request, 'public/catalogo_home.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_actual
    })


"""
    Muestra el detalle de un producto.
"""
def detalle_producto(request, id):
    producto = producto_service.get_by_id(id)
    if not producto:
        return render(request, 'public/no_encontrado.html', status=404)

    # Obtener todos los inventarios
    inventarios = inventario_service.get_all()

    # Buscar cantidad del producto actual
    inventario = next((inv for inv in inventarios if inv.product_id == producto.id), None)
    producto.cantidad = inventario.quantity if inventario else 0

    return render(request, 'public/detalle_producto.html', {
        'producto': producto
    })
