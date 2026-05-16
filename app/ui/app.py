from __future__ import annotations

import flet as ft

from app.db.repositories import DishRepository, IngredientRepository
from app.services.auth_service import AuthService
from app.services.catalog_service import CatalogService
from app.services.stats_service import StatsService
from app.ui.components.dialogs import show_message
from app.ui.pages.dashboard_page import build_dashboard_page
from app.ui.pages.dishes_page import build_dishes_page
from app.ui.pages.ingredients_page import build_ingredients_page
from app.ui.pages.login_page import build_login_page
from app.ui.pages.register_page import build_register_page
from app.ui.pages.stats_page import build_stats_page


class RationApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.current_user = None
        self.auth = AuthService()
        self.ingredients = IngredientRepository()
        self.dishes = DishRepository()
        self.catalog = CatalogService(self.ingredients, self.dishes)
        self.stats = StatsService(self.dishes)

        page.title = "Мой рацион"
        page.window_width = 1100
        page.window_height = 760
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.GREY_100
        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        self.route_change(None)

    def show_message(self, message: str) -> None:
        show_message(self.page, message)

    def navigate(self, route: str) -> None:
        self.page.run_task(self.page.push_route, route)

    def logout(self) -> None:
        self.current_user = None
        self.navigate("/")

    def require_user(self) -> bool:
        if self.current_user is None:
            self.navigate("/")
            return False
        return True

    def route_change(self, _: ft.RouteChangeEvent | None) -> None:
        route = self.page.route or "/"
        self.page.views.clear()

        if route == "/register":
            self.page.views.append(ft.View([build_register_page(self)], route=route))
        elif route == "/dashboard" and self.require_user():
            self.page.views.append(ft.View([self.shell("Главная", build_dashboard_page(self))], route=route))
        elif route == "/ingredients" and self.require_user():
            self.page.views.append(
                ft.View([self.shell("Ингредиенты", build_ingredients_page(self))], route=route)
            )
        elif route == "/dishes" and self.require_user():
            self.page.views.append(ft.View([self.shell("Блюда", build_dishes_page(self))], route=route))
        elif route == "/stats" and self.require_user():
            self.page.views.append(ft.View([self.shell("Статистика", build_stats_page(self))], route=route))
        else:
            self.page.views.append(ft.View([build_login_page(self)], route="/"))
        self.page.update()

    def view_pop(self, _: ft.ViewPopEvent) -> None:
        if len(self.page.views) <= 1:
            self.navigate("/")
            return
        self.page.views.pop()
        self.navigate(self.page.views[-1].route)

    def shell(self, title: str, content: ft.Control) -> ft.Control:
        menu_items = [
            ("Главная", "/dashboard"),
            ("Ингредиенты", "/ingredients"),
            ("Блюда", "/dishes"),
            ("Статистика", "/stats"),
        ]
        return ft.Row(
            [
                ft.Container(
                    width=220,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
                    padding=16,
                    content=ft.Column(
                        [
                            ft.Text("Мой рацион", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                self.current_user.full_name if self.current_user else "",
                                color=ft.Colors.GREY_700,
                            ),
                            ft.Divider(),
                            *[
                                ft.TextButton(
                                    label,
                                    on_click=lambda _, target=target: self.navigate(target),
                                    style=ft.ButtonStyle(
                                        alignment=ft.Alignment.CENTER_LEFT,
                                        bgcolor=(
                                            ft.Colors.GREEN_50
                                            if self.page.route == target
                                            else ft.Colors.TRANSPARENT
                                        ),
                                    ),
                                )
                                for label, target in menu_items
                            ],
                            ft.Container(expand=True),
                            ft.OutlinedButton("Выйти", on_click=lambda _: self.logout()),
                        ],
                        expand=True,
                    ),
                ),
                ft.Container(
                    expand=True,
                    padding=24,
                    content=ft.Column(
                        [
                            ft.Text(title, size=28, weight=ft.FontWeight.BOLD),
                            content,
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )


def _main(page: ft.Page) -> None:
    RationApp(page)


def run() -> None:
    ft.run(_main, no_cdn=True)

