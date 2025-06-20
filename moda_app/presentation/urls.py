from django.urls import path
from django.contrib.auth import views as auth_views

# Vistas públicas
from moda_app.presentation.views.public_view import (
    catalogo_home,
    filtrar_por_categoria,
    detalle_producto
)

# Vistas administrativas
from moda_app.presentation.views.admin_view import (
    admin_home,
    admin_listar_productos,
    admin_listar_categorias,      
    admin_crear_categoria, 
    admin_editar_categoria,
    admin_eliminar_categoria,
    admin_crear_producto,
    admin_editar_producto,
    admin_eliminar_producto,
    admin_listar_inventario,
    admin_editar_inventario,
    
)

urlpatterns = [
    # ----- VISTAS PÚBLICAS -----
    path('', catalogo_home, name='catalogo_home'),
    path('categoria/<int:id>/', filtrar_por_categoria, name='filtrar_por_categoria'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
    

    # ----- LOGIN / LOGOUT -----
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='catalogo_home'), name='logout'),



    # ----- PANEL ADMIN -----
   path('panel/home/', admin_home, name='admin_home'),

    # CRUD PRODUCTOS
    path('panel/productos/', admin_listar_productos, name='admin_listar_productos'),
    path('panel/productos/agregar/', admin_crear_producto, name='admin_crear_producto'),
    path('panel/productos/editar/<int:id>/', admin_editar_producto, name='admin_editar_producto'),
    path('panel/productos/eliminar/<int:id>/', admin_eliminar_producto, name='admin_eliminar_producto'),

    
    # CRUD CATEGORÍAS
    path('panel/categorias/', admin_listar_categorias, name='admin_listar_categorias'),
    path('panel/categorias/agregar/', admin_crear_categoria, name='admin_crear_categoria'),
    path('panel/categorias/editar/<int:id>/', admin_editar_categoria, name='admin_editar_categoria'),
    path('panel/categorias/eliminar/<int:id>/', admin_eliminar_categoria, name='admin_eliminar_categoria'),



    path('panel/inventario/', admin_listar_inventario, name='admin_listar_inventario'),
    path('panel/inventario/editar/<int:id>/', admin_editar_inventario, name='admin_editar_inventario'),


]
