from __future__ import annotations

import flet as ft


def show_message(page: ft.Page, message: str) -> None:
    page.snack_bar = ft.SnackBar(ft.Text(message))
    page.snack_bar.open = True
    page.update()

