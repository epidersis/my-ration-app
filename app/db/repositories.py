from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable

from app.config import DB_PATH
from app.db.database import get_connection
from app.db.models import Dish, DishIngredient, Ingredient, User


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class UserRepository:
    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.db_path = db_path

    def create(self, login: str, full_name: str, password_hash: str) -> User:
        try:
            with get_connection(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO users(login, full_name, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (login.strip(), full_name.strip(), password_hash, _now()),
                )
                user_id = cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Пользователь с таким логином уже существует") from exc
        user = self.get_by_id(int(user_id))
        if user is None:
            raise RuntimeError("Не удалось создать пользователя")
        return user

    def get_by_login(self, login: str) -> User | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE login = ?",
                (login.strip(),),
            ).fetchone()
        return User(**dict(row)) if row else None

    def get_by_id(self, user_id: int) -> User | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return User(**dict(row)) if row else None


class IngredientRepository:
    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.db_path = db_path

    def list_for_user(self, user_id: int) -> list[Ingredient]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT * FROM ingredients
                WHERE user_id = ?
                ORDER BY lower(name)
                """,
                (user_id,),
            ).fetchall()
        return [Ingredient(**dict(row)) for row in rows]

    def get(self, ingredient_id: int, user_id: int) -> Ingredient | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM ingredients WHERE id = ? AND user_id = ?",
                (ingredient_id, user_id),
            ).fetchone()
        return Ingredient(**dict(row)) if row else None

    def create(self, user_id: int, name: str, calories_per_100g: float) -> Ingredient:
        try:
            with get_connection(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO ingredients(user_id, name, calories_per_100g, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, name.strip(), calories_per_100g, _now()),
                )
                ingredient_id = cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Ингредиент с таким названием уже есть в вашей базе") from exc
        ingredient = self.get(int(ingredient_id), user_id)
        if ingredient is None:
            raise RuntimeError("Не удалось создать ингредиент")
        return ingredient

    def update(
        self,
        ingredient_id: int,
        user_id: int,
        name: str,
        calories_per_100g: float,
    ) -> None:
        try:
            with get_connection(self.db_path) as conn:
                conn.execute(
                    """
                    UPDATE ingredients
                    SET name = ?, calories_per_100g = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (name.strip(), calories_per_100g, ingredient_id, user_id),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("Ингредиент с таким названием уже есть в вашей базе") from exc

    def delete(self, ingredient_id: int, user_id: int) -> None:
        with get_connection(self.db_path) as conn:
            used = conn.execute(
                """
                SELECT 1 FROM dish_ingredients di
                JOIN dishes d ON d.id = di.dish_id
                WHERE di.ingredient_id = ? AND d.user_id = ?
                LIMIT 1
                """,
                (ingredient_id, user_id),
            ).fetchone()
            if used:
                raise ValueError("Нельзя удалить ингредиент, который уже используется в блюдах")
            conn.execute(
                "DELETE FROM ingredients WHERE id = ? AND user_id = ?",
                (ingredient_id, user_id),
            )


class DishRepository:
    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.db_path = db_path

    def create(
        self,
        user_id: int,
        name: str,
        description: str,
        total_calories: float,
        items: Iterable[dict[str, float | int]],
    ) -> Dish:
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO dishes(user_id, name, description, total_calories, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, name.strip(), description.strip(), total_calories, _now()),
            )
            dish_id = int(cursor.lastrowid)
            conn.executemany(
                """
                INSERT INTO dish_ingredients(
                    dish_id, ingredient_id, weight_grams, calories_calculated
                )
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        dish_id,
                        int(item["ingredient_id"]),
                        float(item["weight_grams"]),
                        float(item["calories_calculated"]),
                    )
                    for item in items
                ],
            )
        dish = self.get(dish_id, user_id)
        if dish is None:
            raise RuntimeError("Не удалось создать блюдо")
        return dish

    def get(self, dish_id: int, user_id: int) -> Dish | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM dishes WHERE id = ? AND user_id = ?",
                (dish_id, user_id),
            ).fetchone()
        return Dish(**dict(row)) if row else None

    def list_for_user(self, user_id: int) -> list[Dish]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT * FROM dishes
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            ).fetchall()
        return [Dish(**dict(row)) for row in rows]

    def list_for_period(
        self,
        user_id: int,
        start_at: str | None,
        end_at: str | None,
    ) -> list[Dish]:
        query = "SELECT * FROM dishes WHERE user_id = ?"
        params: list[object] = [user_id]
        if start_at:
            query += " AND created_at >= ?"
            params.append(start_at)
        if end_at:
            query += " AND created_at < ?"
            params.append(end_at)
        query += " ORDER BY created_at DESC"
        with get_connection(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
        return [Dish(**dict(row)) for row in rows]

    def list_today(self, user_id: int) -> list[Dish]:
        today = datetime.now().date().isoformat()
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT * FROM dishes
                WHERE user_id = ? AND date(created_at) = date(?)
                ORDER BY created_at DESC
                """,
                (user_id, today),
            ).fetchall()
        return [Dish(**dict(row)) for row in rows]

    def get_items(self, dish_id: int) -> list[DishIngredient]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT
                    di.id,
                    di.dish_id,
                    di.ingredient_id,
                    i.name AS ingredient_name,
                    di.weight_grams,
                    i.calories_per_100g,
                    di.calories_calculated
                FROM dish_ingredients di
                JOIN ingredients i ON i.id = di.ingredient_id
                WHERE di.dish_id = ?
                ORDER BY lower(i.name)
                """,
                (dish_id,),
            ).fetchall()
        return [DishIngredient(**dict(row)) for row in rows]

    def delete(self, dish_id: int, user_id: int) -> None:
        with get_connection(self.db_path) as conn:
            conn.execute("DELETE FROM dishes WHERE id = ? AND user_id = ?", (dish_id, user_id))

