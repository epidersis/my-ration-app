import pytest

from app.services.catalog_service import CatalogService


class IngredientRepositoryStub:
    def get(self, ingredient_id: int, user_id: int):  # noqa: ANN201
        return None


class DishRepositoryStub:
    pass


def test_create_dish_requires_selected_ingredient() -> None:
    service = CatalogService(IngredientRepositoryStub(), DishRepositoryStub())

    with pytest.raises(ValueError, match="Выберите ингредиент"):
        service.create_dish(
            user_id=1,
            name="Каша",
            description="",
            raw_items=[{"ingredient_id": "", "weight_grams": "100"}],
        )
