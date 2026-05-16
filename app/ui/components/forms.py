from __future__ import annotations

import flet as ft


def page_title(text: str) -> ft.Text:
    return ft.Text(text, size=24, weight=ft.FontWeight.BOLD)


def empty_state(text: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, color=ft.Colors.GREY_700),
        padding=20,
        alignment=ft.Alignment.CENTER,
    )


def metric_card(title: str, value: str, subtitle: str | None = None) -> ft.Container:
    controls: list[ft.Control] = [
        ft.Text(title, size=13, color=ft.Colors.GREY_700),
        ft.Text(value, size=26, weight=ft.FontWeight.BOLD),
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=12, color=ft.Colors.GREY_700))
    return ft.Container(
        content=ft.Column(controls, spacing=4),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        padding=16,
        expand=True,
    )

