from __future__ import annotations

import math

import flet as ft

from app.db.models import Dish
from app.services.calorie_service import calories_for_ingredient
from app.ui.components.forms import empty_state


def build_dishes_page(app) -> ft.Control:
    content = ft.Column(spacing=10)

    def refresh(update_page: bool = True) -> None:
        dishes = app.dishes.list_for_user(app.current_user.id)
        rows: list[ft.Control] = []
        if not dishes:
            rows.append(empty_state("Блюда ещё не добавлены"))
        for dish in dishes:
            rows.append(_dish_row(app, dish, refresh))
        content.controls = rows
        if update_page:
            app.page.update()

    add_button = ft.ElevatedButton(
        "Создать блюдо",
        on_click=lambda _: _open_dish_dialog(app, refresh),
    )
    refresh(update_page=False)
    return ft.Column([add_button, content], spacing=16)


def _dish_row(app, dish: Dish, refresh) -> ft.Control:
    items = app.dishes.get_items(dish.id)
    ingredients_text = ", ".join(
        f"{item.ingredient_name} {item.weight_grams:g} г" for item in items
    )
    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        padding=12,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(dish.name, weight=ft.FontWeight.BOLD),
                        ft.Text(dish.description or "Без описания", color=ft.Colors.GREY_700),
                        ft.Text(ingredients_text, size=12),
                    ],
                    expand=True,
                    spacing=3,
                ),
                ft.Text(f"{dish.total_calories:.1f} ккал", weight=ft.FontWeight.BOLD),
                ft.OutlinedButton("Удалить", on_click=lambda _: _delete_dish(app, dish, refresh)),
            ],
            spacing=12,
        ),
    )


def _open_dish_dialog(app, refresh) -> None:
    ingredients = app.ingredients.list_for_user(app.current_user.id)
    if not ingredients:
        app.show_message("Сначала добавьте хотя бы один ингредиент")
        return

    name = ft.TextField(label="Название блюда")
    description = ft.TextField(label="Описание", multiline=True, min_lines=2, max_lines=3)
    rows = ft.Column(spacing=8)
    total_text = ft.Text("Итого: 0.0 ккал", weight=ft.FontWeight.BOLD)
    error = ft.Text(color=ft.Colors.RED_700)
    row_state: list[dict[str, ft.Control]] = []

    def close() -> None:
        app.page.pop_dialog()

    def recalc(_: ft.ControlEvent | None = None) -> None:
        total = 0.0
        for state in row_state:
            ingredient_id = state["ingredient"].value
            weight_value = state["weight"].value
            if not ingredient_id or not weight_value:
                continue
            ingredient = next((item for item in ingredients if str(item.id) == ingredient_id), None)
            if ingredient is None:
                continue
            try:
                weight = float(str(weight_value).replace(",", "."))
            except ValueError:
                continue
            if math.isfinite(weight) and weight > 0:
                total += calories_for_ingredient(ingredient.calories_per_100g, weight)
        total_text.value = f"Итого: {total:.1f} ккал"
        app.page.update()

    def rebuild_rows(update_page: bool = True) -> None:
        rows.controls = [
            ft.Row(
                [
                    state["ingredient"],
                    state["weight"],
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="Удалить строку",
                        on_click=lambda _, st=state: remove_row(st),
                    ),
                ],
                spacing=8,
            )
            for state in row_state
        ]
        if update_page:
            app.page.update()

    def add_row(_: ft.ControlEvent | None = None, update_page: bool = True) -> None:
        dropdown = ft.Dropdown(
            label="Ингредиент",
            options=[ft.dropdown.Option(str(item.id), item.name) for item in ingredients],
            width=280,
            on_select=recalc,
        )
        weight = ft.TextField(
            label="Вес, г",
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=recalc,
        )
        row_state.append({"ingredient": dropdown, "weight": weight})
        rebuild_rows(update_page=update_page)

    def remove_row(state: dict[str, ft.Control]) -> None:
        if len(row_state) > 1:
            row_state.remove(state)
            rebuild_rows()
            recalc()

    def save(_: ft.ControlEvent) -> None:
        raw_items = [
            {
                "ingredient_id": str(state["ingredient"].value or ""),
                "weight_grams": str(state["weight"].value or ""),
            }
            for state in row_state
            if state["ingredient"].value or state["weight"].value
        ]
        try:
            app.catalog.create_dish(
                app.current_user.id,
                name.value or "",
                description.value or "",
                raw_items,
            )
        except (ValueError, TypeError) as exc:
            error.value = str(exc)
            app.page.update()
            return
        close()
        refresh()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Создание блюда"),
        content=ft.Container(
            width=560,
            height=520,
            content=ft.Column(
                [
                    name,
                    description,
                    ft.Row(
                        [
                            ft.Text("Ингредиенты", weight=ft.FontWeight.BOLD),
                            ft.TextButton("Добавить строку", on_click=add_row),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    rows,
                    total_text,
                    error,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            ),
        ),
        actions=[
            ft.TextButton("Отмена", on_click=lambda _: close()),
            ft.ElevatedButton("Сохранить", on_click=save),
        ],
    )
    add_row(update_page=False)
    app.page.show_dialog(dialog)


def _delete_dish(app, dish: Dish, refresh) -> None:
    app.dishes.delete(dish.id, app.current_user.id)
    refresh()
