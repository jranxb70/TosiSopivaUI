import flet as ft
from flet import *

class AppBar(ft.UserControl):
    def change_theme(self, e):
        page = e.page
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    def exit_app(self, e):
        page = e.page
        page.window_destroy()
        
    def go_home(self, e):
        page = e.page
        page.go('/')

    def build(self):
        app_bar = ft.AppBar(
            leading=ft.IconButton(ft.icons.ACCOUNT_BALANCE, on_click=self.go_home),
            leading_width=40,
            title = ft.Text('Tosi Sopiva Laskutus'),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=self.change_theme),
                ft.IconButton(ft.icons.EXIT_TO_APP, on_click=self.exit_app),
                ft.SubmenuButton(
            leading=ft.Icon(ft.icons.LANGUAGE),
            controls=[
                ft.MenuItemButton(
                    content=ft.Text("English"),
                    close_on_click=False,
                    # on_click=translateToEn
                ),
                ft.MenuItemButton(
                    content=ft.Text("Suomi"),
                    close_on_click=False,
                    # on_click=translateToFi
                ),
                ]
            ),
                ]
            )
        return app_bar