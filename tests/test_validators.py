import pytest

from app.utils.validators import (
    validate_calories_per_100g,
    validate_ingredient_name,
    validate_passwords,
    validate_weight,
)


def test_empty_ingredient_name() -> None:
    with pytest.raises(ValueError, match="Нельзя оставлять поле названия"):
        validate_ingredient_name(" ")


def test_calories_must_be_positive() -> None:
    with pytest.raises(ValueError, match="Калорийность должна быть больше 0"):
        validate_calories_per_100g(0)


def test_weight_must_be_positive() -> None:
    with pytest.raises(ValueError, match="Вес должен быть больше 0"):
        validate_weight(-10)


def test_passwords_must_match() -> None:
    with pytest.raises(ValueError, match="Пароли не совпадают"):
        validate_passwords("secret", "different")

