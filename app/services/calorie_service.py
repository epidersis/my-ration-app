from __future__ import annotations


def calories_for_ingredient(calories_per_100g: float, weight_grams: float) -> float:
    return calories_per_100g * weight_grams / 100


def dish_total_calories(items: list[dict[str, float]]) -> float:
    return sum(
        calories_for_ingredient(item["calories_per_100g"], item["weight_grams"])
        for item in items
    )

