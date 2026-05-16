from __future__ import annotations


def validate_required(value: str, message: str) -> None:
    if not value or not value.strip():
        raise ValueError(message)


def parse_positive_float(value: str | float | int, message: str) -> float:
    try:
        parsed = float(str(value).replace(",", "."))
    except (TypeError, ValueError) as exc:
        raise ValueError(message) from exc
    if parsed <= 0:
        raise ValueError(message)
    return parsed


def validate_ingredient_name(name: str) -> None:
    validate_required(
        name,
        "Нельзя оставлять поле названия ингредиента пустым. Заполните поле 😊",
    )


def validate_dish_name(name: str) -> None:
    validate_required(name, "Название блюда не должно быть пустым. Введите название")


def validate_calories_per_100g(value: str | float | int) -> float:
    return parse_positive_float(value, "Калорийность должна быть больше 0")


def validate_weight(value: str | float | int) -> float:
    return parse_positive_float(value, "Вес должен быть больше 0")


def validate_passwords(password: str, password_repeat: str) -> None:
    if password != password_repeat:
        raise ValueError("Пароли не совпадают")

