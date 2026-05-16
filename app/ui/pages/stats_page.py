from __future__ import annotations

import flet as ft

from app.ui.components.forms import empty_state, metric_card


PERIODS = {
    "day": "День",
    "week": "Неделя",
    "month": "Месяц",
    "year": "Год",
    "all": "Весь период",
}


def build_stats_page(app) -> ft.Control:
    period = ft.Dropdown(
        label="Период",
        value="day",
        options=[ft.dropdown.Option(key, label) for key, label in PERIODS.items()],
        width=220,
    )
    content = ft.Column(spacing=12)

    def refresh(_: ft.ControlEvent | None = None, update_page: bool = True) -> None:
        dishes = app.stats.get_period_dishes(app.current_user.id, period.value or "day")
        summary = app.stats.summarize(dishes)
        if not dishes:
            content.controls = [empty_state("Нет данных, добавьте блюда для формирования графика")]
        else:
            by_day = summary["by_day"]
            max_value = max(by_day.values()) if by_day else 1
            day_rows = [
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(day, width=110),
                                ft.Container(
                                    height=12,
                                    expand=True,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=6,
                                    width=max(40, int(360 * calories / max_value)),
                                ),
                                ft.Text(f"{calories:.1f} ккал", width=110),
                            ],
                            spacing=8,
                        )
                    ]
                )
                for day, calories in by_day.items()
            ]
            dish_rows = [
                ft.ListTile(
                    title=ft.Text(dish.name),
                    subtitle=ft.Text(dish.created_at[:16].replace("T", " ")),
                    trailing=ft.Text(f"{dish.total_calories:.1f} ккал"),
                )
                for dish in dishes
            ]
            content.controls = [
                ft.Row(
                    [
                        metric_card("Сумма за период", f"{summary['total']:.1f}", "ккал"),
                        metric_card("Количество блюд", str(len(dishes))),
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
                            ft.Text("Калории по дням", size=18, weight=ft.FontWeight.BOLD),
                            *day_rows,
                        ],
                        spacing=10,
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=8,
                    content=ft.Column(
                        [
                            ft.Text("Блюда за период", size=18, weight=ft.FontWeight.BOLD),
                            *dish_rows,
                        ],
                        spacing=4,
                    ),
                ),
            ]
        if update_page:
            app.page.update()

    period.on_select = refresh
    refresh(update_page=False)
    return ft.Column([period, content], spacing=16)
