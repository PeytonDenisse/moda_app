from django.shortcuts import render, get_object_or_404
from moda_app.service.product_service import ProductService
from moda_app.service.category_service import CategoryService

# Servicios
producto_service = ProductService()
categoria_service = CategoryService()

"""
    Vista pública
    Muestra todos los productos y las categorías
"""

def catalogo_home(request):
    
    productos = producto_service.get_all()
    categorias = categoria_service.get_all()
    return render(request, 'public/catalogo_home.html', {
        'productos': productos,
        'categorias': categorias
    })



"""
    Muestra productos filtrados por categoría.
"""

def filtrar_por_categoria(request, id):
    productos = [p for p in producto_service.get_all() if p.id_categoria == id]
    categorias = categoria_service.get_all()
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
    return render(request, 'public/detalle_producto.html', {
        'producto': producto
    })
