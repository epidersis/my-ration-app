"""Flet UI layer."""

import flet as ft


if not hasattr(ft, "Colors") and hasattr(ft, "colors"):
    ft.Colors = ft.colors

if not hasattr(ft, "Icons") and hasattr(ft, "icons"):
    ft.Icons = ft.icons
