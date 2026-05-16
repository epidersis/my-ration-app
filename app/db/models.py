from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    login: str
    full_name: str
    password_hash: str
    created_at: str


@dataclass(frozen=True)
class Ingredient:
    id: int
    user_id: int
    name: str
    calories_per_100g: float
    created_at: str


@dataclass(frozen=True)
class Dish:
    id: int
    user_id: int
    name: str
    description: str
    total_calories: float
    created_at: str


@dataclass(frozen=True)
class DishIngredient:
    id: int
    dish_id: int
    ingredient_id: int
    ingredient_name: str
    weight_grams: float
    calories_per_100g: float
    calories_calculated: float

