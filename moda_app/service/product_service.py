"""
Los servicios implementan la lógica de negocio de productos.
"""
from typing import List, Optional
from moda_app.domain.schema import ProductEntity
from moda_app.persistence.repositories import ProductRepository

class ProductService:
    def __init__(self, repository=None):
        self.repository = repository or ProductRepository()

    def get_all(self) -> List[ProductEntity]:
        return self.repository.get_all()

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        return self.repository.get_by_id(product_id)

    def create(self, entity: ProductEntity) -> ProductEntity:
        return self.repository.create(entity)

    def update(self, entity: ProductEntity) -> Optional[ProductEntity]:
        return self.repository.update(entity)

    def delete(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
