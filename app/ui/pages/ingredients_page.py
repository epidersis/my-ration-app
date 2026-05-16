from __future__ import annotations

import flet as ft

from app.db.models import Ingredient
from app.ui.components.forms import empty_state


def build_ingredients_page(app) -> ft.Control:
    content = ft.Column(spacing=10)

    def refresh(update_page: bool = True) -> None:
        ingredients = app.ingredients.list_for_user(app.current_user.id)
        rows: list[ft.Control] = []
        if not ingredients:
            rows.append(empty_state("Ингредиенты ещё не добавлены"))
        for ingredient in ingredients:
            rows.append(_ingredient_row(app, ingredient, refresh))
        content.controls = rows
        if update_page:
            app.page.update()

    add_button = ft.ElevatedButton(
        "Добавить ингредиент",
        on_click=lambda _: _open_ingredient_dialog(app, None, refresh),
    )
    refresh(update_page=False)
    return ft.Column([add_button, content], spacing=16)


def _ingredient_row(app, ingredient: Ingredient, refresh) -> ft.Control:
    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        padding=12,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(ingredient.name, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{ingredient.calories_per_100g:.1f} ккал на 100 г"),
                    ],
                    expand=True,
                    spacing=2,
                ),
                ft.TextButton(
                    "Изменить",
                    on_click=lambda _: _open_ingredient_dialog(app, ingredient, refresh),
                ),
                ft.OutlinedButton(
                    "Удалить",
                    on_click=lambda _: _delete_ingredient(app, ingredient, refresh),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )


def _open_ingredient_dialog(app, ingredient: Ingredient | None, refresh) -> None:
    name = ft.TextField(label="Название", value=ingredient.name if ingredient else "")
    calories = ft.TextField(
        label="Калорийность на 100 г",
        value=str(ingredient.calories_per_100g) if ingredient else "",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    error = ft.Text(color=ft.Colors.RED_700)

    def close() -> None:
        app.page.pop_dialog()

    def save(_: ft.ControlEvent) -> None:
        try:
            if ingredient:
                app.catalog.update_ingredient(
                    ingredient.id,
                    app.current_user.id,
                    name.value or "",
                    calories.value or "",
                )
            else:
                app.catalog.create_ingredient(
                    app.current_user.id,
                    name.value or "",
                    calories.value or "",
                )
        except ValueError as exc:
            error.value = str(exc)
            app.page.update()
            return
        close()
        refresh()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ингредиент"),
        content=ft.Column([name, calories, error], tight=True, width=420),
        actions=[
            ft.TextButton("Отмена", on_click=lambda _: close()),
            ft.ElevatedButton("Сохранить", on_click=save),
        ],
    )
    app.page.show_dialog(dialog)


def _delete_ingredient(app, ingredient: Ingredient, refresh) -> None:
    try:
        app.ingredients.delete(ingredient.id, app.current_user.id)
    except ValueError as exc:
        app.show_message(str(exc))
        return
    refresh()
