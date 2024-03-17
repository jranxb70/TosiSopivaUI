import flet as ft
from flet_route import Params, Basket
from flet import *

def Home(page: ft.Page, params: Params, basket: Basket):
    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()
        
    def exit_app(e):
        page = e.page
        page.window_destroy()
        
    return ft.View(
        "/",
        
       controls=[
            ft.AppBar(
                leading=ft.Icon(ft.icons.ACCOUNT_BALANCE),
                leading_width=40,
                title=ft.Text("TosiSopivaLaskutus"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=change_theme),
                    ft.SubmenuButton(
                        leading=ft.Icon(ft.icons.LANGUAGE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("English"),
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Suomi"),
                            )
                        ]
                    ),
                    ft.IconButton(ft.icons.EXIT_TO_APP, on_click=exit_app),
                ],
            ),
            Text(value='TosiSopivaLaskutus', size=30),
            ElevatedButton(text='Registration', on_click=lambda _:page.go('/page_reg')),
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )