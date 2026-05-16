from __future__ import annotations

import flet as ft


def build_login_page(app) -> ft.Control:
    login = ft.TextField(label="Логин", autofocus=True)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED_700)

    def submit(_: ft.ControlEvent) -> None:
        user = app.auth.authenticate(login.value or "", password.value or "")
        if user is None:
            error.value = "Неверный логин или пароль. Проверьте данные и повторите ввод."
            app.page.update()
            return
        app.current_user = user
        app.page.go("/dashboard")

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=420,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=28,
            content=ft.Column(
                [
                    ft.Text("Мой рацион", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Вход в приложение", color=ft.Colors.GREY_700),
                    login,
                    password,
                    error,
                    ft.ElevatedButton("Войти", on_click=submit, width=420),
                    ft.TextButton(
                        "Зарегистрироваться",
                        on_click=lambda _: app.page.go("/register"),
                    ),
                ],
                spacing=14,
                tight=True,
            ),
        ),
    )

