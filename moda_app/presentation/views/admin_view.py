from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from moda_app.service.product_service import ProductService
from moda_app.domain.schema import ProductEntity
from moda_app.service.category_service import CategoryService
from moda_app.domain.schema import CategoryEntity
from moda_app.service.inventario_service import InventoryService
from moda_app.domain.schema import InventoryEntity


producto_service = ProductService()
categoria_service = CategoryService()
inventario_service = InventoryService()


"""Vista principal del panel admin con accesos rápidos."""

@login_required
def admin_home(request):
    return render(request, 'admin/admin_home.html')



"""Lista todos los productos para administrarlos."""
@login_required
def admin_listar_productos(request):
    productos = producto_service.get_all()
    categorias = categoria_service.get_all()
    inventarios = inventario_service.get_all()
    
    inventario_por_producto = {inv.product_id: inv for inv in inventarios}

    productos_con_inventario = []
    for prod in productos:
        prod_inventario = inventario_por_producto.get(prod.id)
        productos_con_inventario.append({
            'producto': prod,
            'inventario': prod_inventario
        })

    return render(request, 'admin/productos/listar.html', {
        'productos_con_inventario': productos_con_inventario,
        'categorias': categorias
    })



"""Formulario para crear un nuevo producto """
@login_required
def admin_crear_producto(request):
    categorias = categoria_service.get_all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        id_categoria = int(request.POST.get('id_categoria'))
        disponibilidad = request.POST.get('disponibilidad') == 'on'
        price = float(request.POST.get('price'))
        image = request.POST.get('image')

        nuevo = ProductEntity(
            id=None,
            name=name,
            description=description,
            id_categoria=id_categoria,
            disponibilidad=disponibilidad,
            price=price,
            image=image,
            last_updated=None
        )

        producto_creado = producto_service.create(nuevo)

        # Crear inventario con cantidad 0 y estado "Disponible"
        nuevo_inventario = InventoryEntity(
            id=None,  # aquí pasas None para que se cree uno nuevo
            product_id=producto_creado.id,
            category_id=producto_creado.id_categoria,
            quantity=0,
            status="Disponible",
            last_updated=None
        )
        inventario_service.create(nuevo_inventario)

        messages.success(request, "Producto e inventario creados correctamente.")
        return redirect('admin_listar_productos')

    return render(request, 'admin/productos/crear.html', {
        'categorias': categorias
    })




"""Formulario para editar un producto existente."""
@login_required
def admin_editar_producto(request, id):
    producto = producto_service.get_by_id(id)
    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('admin_listar_productos')

    categorias = categoria_service.get_all()

    if request.method == 'POST':
        producto.name = request.POST.get('name')
        producto.description = request.POST.get('description')
        producto.id_categoria = int(request.POST.get('id_categoria'))
        producto.disponibilidad = request.POST.get('disponibilidad') == 'on'
        producto.price = float(request.POST.get('price'))
        image = request.POST.get('image')
        if image:
            producto.image = image

        producto_service.update(producto)
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('admin_listar_productos')

    return render(request, 'admin/productos/editar.html', {
        'producto': producto,
        'categorias': categorias
    })


"""Elimina un producto existente."""
@login_required
def admin_eliminar_producto(request, id):
    producto = producto_service.get_by_id(id)
    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('admin_listar_productos')

    if request.method == 'POST':
        producto_service.delete(id)
        messages.success(request, "Producto eliminado.")
        return redirect('admin_listar_productos')

    return render(request, 'admin/productos/eliminar.html', {
        'producto': producto
    })







# LISTAR CATEGORÍAS
# ───────────────────────────────────────────────
@login_required
def admin_listar_categorias(request):
    categorias = categoria_service.get_all()
    return render(request, 'admin/categorias/listar.html', {
        'categorias': categorias
    })

# CREAR NUEVA CATEGORÍA
@login_required
def admin_crear_categoria(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        nueva = CategoryEntity(id=None, name=name, description=description)
        categoria_service.create(nueva)

        messages.success(request, "Categoría creada correctamente.")
        return redirect('admin_listar_categorias')

    return render(request, 'admin/categorias/crear.html')

# EDITAR CATEGORÍA EXISTENTE

@login_required
def admin_editar_categoria(request, id):
    categoria = categoria_service.get_by_id(id)
    if not categoria:
        messages.error(request, "Categoría no encontrada.")
        return redirect('admin_listar_categorias')

    if request.method == 'POST':
        categoria.name = request.POST.get('name')
        categoria.description = request.POST.get('description')

        categoria_service.update(categoria)
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect('admin_listar_categorias')

    return render(request, 'admin/categorias/editar.html', {
        'categoria': categoria
    })

# ELIMINAR CATEGORÍA 
@login_required
def admin_eliminar_categoria(request, id):
    categoria = categoria_service.get_by_id(id)
    if not categoria:
        messages.error(request, "Categoría no encontrada.")
        return redirect('admin_listar_categorias')

    if request.method == 'POST':
        categoria_service.delete(id)
        messages.success(request, "Categoría eliminada exitosamente.")
        return redirect('admin_listar_categorias')

    return render(request, 'admin/categorias/eliminar.html', {
        'categoria': categoria
    })


"""Lista el inventario de productos."""

@login_required
def admin_listar_inventario(request):
    inventario = inventario_service.get_all()
    return render(request, 'admin/inventario/listar.html', {
        'inventario': inventario
    })



@login_required
def admin_editar_inventario(request, id):
    inventario = inventario_service.get_by_product_id(id)

    if not inventario:
        messages.error(request, "No hay inventario registrado para este producto.")
        next_url = request.GET.get('next')
        if next_url == 'productos':
            return redirect('admin_listar_productos')
        else:
            return redirect('admin_listar_inventario')

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('quantity'))
        except (TypeError, ValueError):
            messages.error(request, "Cantidad inválida.")
            return redirect('admin_editar_inventario', id=id)

        if cantidad < 0:
            messages.error(request, "La cantidad no puede ser negativa.")
            return redirect('admin_editar_inventario', id=id)

        status = "Agotado" if cantidad == 0 else "Disponible"

        inventario.quantity = cantidad
        inventario.status = status
        inventario_service.update(inventario)

        messages.success(request, "Inventario actualizado correctamente.")

        # Leer next de POST o GET para redireccionar
        next_url = request.POST.get('next', request.GET.get('next'))
        if next_url == 'productos':
            return redirect('admin_listar_productos')
        else:
            return redirect('admin_listar_inventario')

    producto = producto_service.get_by_id(inventario.product_id)
    producto_nombre = producto.name if producto else "Producto desconocido"

    return render(request, 'admin/inventario/editar.html', {
        'inventario': inventario,
        'producto_nombre': producto_nombre,
        'next': request.GET.get('next', 'inventario'), 
    })