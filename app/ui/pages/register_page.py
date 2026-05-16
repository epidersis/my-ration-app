from __future__ import annotations

import flet as ft


def build_register_page(app) -> ft.Control:
    login = ft.TextField(label="Логин", autofocus=True)
    full_name = ft.TextField(label="ФИО / имя пользователя")
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True)
    password_repeat = ft.TextField(label="Повторите пароль", password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED_700)

    def submit(_: ft.ControlEvent) -> None:
        try:
            app.auth.register(
                login.value or "",
                full_name.value or "",
                password.value or "",
                password_repeat.value or "",
            )
        except ValueError as exc:
            error.value = str(exc)
            app.page.update()
            return
        app.show_message("Регистрация выполнена. Теперь войдите в приложение.")
        app.page.go("/")

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=460,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=28,
            content=ft.Column(
                [
                    ft.Text("Регистрация", size=28, weight=ft.FontWeight.BOLD),
                    login,
                    full_name,
                    password,
                    password_repeat,
                    error,
                    ft.ElevatedButton("Зарегистрироваться", on_click=submit, width=460),
                    ft.TextButton("Назад ко входу", on_click=lambda _: app.page.go("/")),
                ],
                spacing=14,
                tight=True,
            ),
        ),
    )

