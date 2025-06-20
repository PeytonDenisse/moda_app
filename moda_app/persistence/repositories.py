from typing import List, Optional
from moda_app.persistence.models import Product, Category, Inventory
from moda_app.domain.schema import ProductEntity, CategoryEntity, InventoryEntity

# REPOSITORIO DE PRODUCTOS
# --------------------------
class ProductRepository:

    @staticmethod
    def get_all() -> List[ProductEntity]:
        productos = Product.objects.all()
        return [
            ProductEntity(
                id=p.id,
                name=p.name,
                description=p.description,
                id_categoria=p.id_categoria.id,
                disponibilidad=p.disponibilidad,
                price=float(p.price),
                last_updated=p.last_updated,
                image=p.image,

            ) for p in productos
        ]

    @staticmethod
    def get_by_id(product_id: int) -> Optional[ProductEntity]:
        try:
            p = Product.objects.get(id=product_id)
            return ProductEntity(
                id=p.id,
                name=p.name,
                description=p.description,
                id_categoria=p.id_categoria.id,
                disponibilidad=p.disponibilidad,
                price=float(p.price),
                image=p.image,

                last_updated=p.last_updated
            )
        except Product.DoesNotExist:
            return None

    @staticmethod
    def create(entity: ProductEntity) -> ProductEntity:
        categoria = Category.objects.get(id=entity.id_categoria)
        p = Product.objects.create(
            name=entity.name,
            description=entity.description,
            id_categoria=categoria,
            disponibilidad=entity.disponibilidad,
            price=entity.price,
            image=entity.image
        )
        entity.id = p.id
        return entity

    @staticmethod
    def update(entity: ProductEntity) -> Optional[ProductEntity]:
        try:
            p = Product.objects.get(id=entity.id)
            p.name = entity.name
            p.description = entity.description
            p.id_categoria_id = entity.id_categoria
            p.disponibilidad = entity.disponibilidad
            p.price = entity.price
            p.image = entity.image
            p.save()
            return entity
        except Product.DoesNotExist:
            return None

    @staticmethod
    def delete(product_id: int) -> bool:
        try:
            Product.objects.get(id=product_id).delete()
            return True
        except Product.DoesNotExist:
            return False


# --------------------------
# REPOSITORIO DE CATEGORÍAS
# --------------------------
class CategoryRepository:

    @staticmethod
    def get_all() -> List[CategoryEntity]:
        categorias = Category.objects.all()
        return [
            CategoryEntity(
                id=c.id,
                name=c.name,
                description=c.description
            ) for c in categorias
        ]

    @staticmethod
    def get_by_id(category_id: int) -> Optional[CategoryEntity]:
        try:
            c = Category.objects.get(id=category_id)
            return CategoryEntity(
                id=c.id,
                name=c.name,
                description=c.description
            )
        except Category.DoesNotExist:
            return None

    @staticmethod
    def create(entity: CategoryEntity) -> CategoryEntity:
        c = Category.objects.create(
            name=entity.name,
            description=entity.description
        )
        entity.id = c.id
        return entity

    @staticmethod
    def update(entity: CategoryEntity) -> Optional[CategoryEntity]:
        try:
            c = Category.objects.get(id=entity.id)
            c.name = entity.name
            c.description = entity.description
            c.save()
            return entity
        except Category.DoesNotExist:
            return None

    @staticmethod
    def delete(category_id: int) -> bool:
        try:
            Category.objects.get(id=category_id).delete()
            return True
        except Category.DoesNotExist:
            return False


# --------------------------
# REPOSITORIO DE INVENTARIO
# --------------------------
class InventoryRepository:

    @staticmethod
    def get_all() -> List[InventoryEntity]:
        inventarios = Inventory.objects.select_related('product', 'category').all()
        return [
            InventoryEntity(
                id=inv.id,
                product_id=inv.product.id,
                category_id=inv.category.id,
                quantity=inv.quantity,
                status=inv.status,
                last_updated=inv.last_updated,
                product=inv.product, 
                category=inv.category    
            ) for inv in inventarios
        ]

    @staticmethod
    def get_by_id(inventory_id: int) -> Optional[InventoryEntity]:
        try:
            inv = Inventory.objects.get(id=inventory_id)
            return InventoryEntity(
                id=inv.id,
                product_id=inv.product.id,
                category_id=inv.category.id,
                quantity=inv.quantity,
                status=inv.status,
                last_updated=inv.last_updated
            )
        except Inventory.DoesNotExist:
            return None

    @staticmethod
    def create(entity: InventoryEntity) -> InventoryEntity:
        product = Product.objects.get(id=entity.product_id)
        category = Category.objects.get(id=entity.category_id)
        inv = Inventory.objects.create(
            product=product,
            category=category,
            quantity=entity.quantity,
            status=entity.status
        )
        entity.id = inv.id
        return entity

    @staticmethod
    def update(entity: InventoryEntity) -> Optional[InventoryEntity]:
        try:
            inv = Inventory.objects.get(id=entity.id)
            inv.quantity = entity.quantity
            inv.status = entity.status
            inv.save()
            return entity
        except Inventory.DoesNotExist:
            return None

    @staticmethod
    def delete(inventory_id: int) -> bool:
        try:
            Inventory.objects.get(id=inventory_id).delete()
            return True
        except Inventory.DoesNotExist:
            return False
