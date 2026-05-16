from app.services.calorie_service import calories_for_ingredient, dish_total_calories


def test_calories_for_ingredient_formula() -> None:
    assert calories_for_ingredient(370, 50) == 185


def test_dish_total_calories() -> None:
    items = [
        {"calories_per_100g": 370, "weight_grams": 50},
        {"calories_per_100g": 90, "weight_grams": 100},
        {"calories_per_100g": 60, "weight_grams": 200},
    ]

    assert dish_total_calories(items) == 395

