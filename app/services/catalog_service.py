from __future__ import annotations

from app.db.models import Dish, Ingredient
from app.db.repositories import DishRepository, IngredientRepository
from app.services.calorie_service import calories_for_ingredient
from app.utils.validators import (
    parse_positive_float,
    validate_dish_name,
    validate_ingredient_name,
)


class CatalogService:
    def __init__(
        self,
        ingredients: IngredientRepository | None = None,
        dishes: DishRepository | None = None,
    ) -> None:
        self.ingredients = ingredients or IngredientRepository()
        self.dishes = dishes or DishRepository()

    def create_ingredient(self, user_id: int, name: str, calories_per_100g: str) -> Ingredient:
        validate_ingredient_name(name)
        calories = parse_positive_float(
            calories_per_100g,
            "Калорийность должна быть больше 0",
        )
        return self.ingredients.create(user_id, name, calories)

    def update_ingredient(
        self,
        ingredient_id: int,
        user_id: int,
        name: str,
        calories_per_100g: str,
    ) -> None:
        validate_ingredient_name(name)
        calories = parse_positive_float(
            calories_per_100g,
            "Калорийность должна быть больше 0",
        )
        self.ingredients.update(ingredient_id, user_id, name, calories)

    def create_dish(
        self,
        user_id: int,
        name: str,
        description: str,
        raw_items: list[dict[str, str]],
    ) -> Dish:
        validate_dish_name(name)
        if not raw_items:
            raise ValueError("Блюдо должно содержать хотя бы один ингредиент")

        prepared: list[dict[str, float | int]] = []
        total = 0.0
        for raw_item in raw_items:
            try:
                ingredient_id = int(raw_item["ingredient_id"])
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError("Выберите ингредиент") from exc
            ingredient = self.ingredients.get(ingredient_id, user_id)
            if ingredient is None:
                raise ValueError("Выбранный ингредиент не найден")
            try:
                raw_weight = raw_item["weight_grams"]
            except KeyError as exc:
                raise ValueError("Вес должен быть больше 0") from exc
            weight = parse_positive_float(raw_weight, "Вес должен быть больше 0")
            calculated = calories_for_ingredient(ingredient.calories_per_100g, weight)
            total += calculated
            prepared.append(
                {
                    "ingredient_id": ingredient.id,
                    "weight_grams": weight,
                    "calories_calculated": calculated,
                }
            )
        return self.dishes.create(user_id, name, description, round(total, 2), prepared)

