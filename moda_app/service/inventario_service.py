from typing import List, Optional
from moda_app.domain.schema import InventoryEntity
from moda_app.persistence.repositories import InventoryRepository

class InventoryService:
    def __init__(self, repository=None):
        self.repository = repository or InventoryRepository()

    def get_all(self) -> List[InventoryEntity]:
        return self.repository.get_all()

    def get_by_id(self, inventory_id: int) -> Optional[InventoryEntity]:
        return self.repository.get_by_id(inventory_id)

    def create(self, entity: InventoryEntity) -> InventoryEntity:
        return self.repository.create(entity)

    def update(self, entity: InventoryEntity) -> Optional[InventoryEntity]:
        return self.repository.update(entity)

    def delete(self, inventory_id: int) -> bool:
        return self.repository.delete(inventory_id)

    def get_by_product_id(self, product_id: int) -> Optional[InventoryEntity]:
        inventarios = self.repository.get_all()
        for inv in inventarios:
            if inv.product_id == product_id:
                return inv
        return None
