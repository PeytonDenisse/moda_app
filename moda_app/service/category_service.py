from typing import List, Optional
from moda_app.domain.schema import CategoryEntity
from moda_app.persistence.repositories import CategoryRepository

class CategoryService:
    def __init__(self, repository=None):
        self.repository = repository or CategoryRepository()

    def get_all(self) -> List[CategoryEntity]:
        return self.repository.get_all()

    def get_by_id(self, category_id: int) -> Optional[CategoryEntity]:
        return self.repository.get_by_id(category_id)

    def create(self, entity: CategoryEntity) -> CategoryEntity:
        return self.repository.create(entity)

    def update(self, entity: CategoryEntity) -> Optional[CategoryEntity]:
        return self.repository.update(entity)

    def delete(self, category_id: int) -> bool:
        return self.repository.delete(category_id)
