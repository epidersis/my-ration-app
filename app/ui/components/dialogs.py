from __future__ import annotations

import flet as ft


def show_message(page: ft.Page, message: str) -> None:
    page.show_dialog(ft.SnackBar(ft.Text(message)))

