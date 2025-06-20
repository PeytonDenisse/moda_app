from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from moda_app.persistence.models import Product, Category

# Producto
@dataclass
class ProductEntity:
    id: Optional[int]
    name: str
    description: str
    id_categoria: int
    disponibilidad: bool
    price: float
    image: Optional[str]  
    last_updated: datetime


# Categoría
@dataclass
class CategoryEntity:
    id: Optional[int]
    name: str
    description: str

# Inventario
@dataclass
class InventoryEntity:
    id: Optional[int]
    product_id: int
    category_id: int
    quantity: int
    status: str
    last_updated: datetime
    product: Optional[Product] = None    
    category: Optional[Category] = None  
