from __future__ import annotations

import flet as ft

from app.services.recommendation_service import get_daily_recommendation
from app.ui.components.forms import empty_state, metric_card


def build_dashboard_page(app) -> ft.Control:
    dishes = app.dishes.list_today(app.current_user.id)
    total = round(sum(dish.total_calories for dish in dishes), 2)
    recommendation = get_daily_recommendation(total if dishes else None, bool(dishes))

    dish_controls: list[ft.Control]
    if dishes:
        dish_controls = [
            ft.ListTile(
                title=ft.Text(dish.name),
                subtitle=ft.Text((dish.description or "Без описания")[:90]),
                trailing=ft.Text(f"{dish.total_calories:.1f} ккал"),
            )
            for dish in dishes
        ]
    else:
        dish_controls = [empty_state("Сегодня блюд пока нет")]

    return ft.Column(
        [
            ft.Row(
                [
                    metric_card("Калории за сегодня", f"{total:.1f}", "ккал"),
                    metric_card("Блюд за сегодня", str(len(dishes))),
                ],
                spacing=12,
            ),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                padding=16,
                content=ft.Column(
                    [
                        ft.Text("Рекомендация", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(recommendation),
                    ],
                    spacing=8,
                ),
            ),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                padding=8,
                content=ft.Column(
                    [
                        ft.Text("Блюда за сегодня", size=18, weight=ft.FontWeight.BOLD),
                        *dish_controls,
                    ],
                    spacing=4,
                ),
            ),
        ],
        spacing=16,
    )

