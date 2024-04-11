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
        def close_dialog(e):
            alert_dialog.open = False
            alert_dialog.update()
            
        def open_dialog(e):
            page = e.page
            page.dialog = alert_dialog
            alert_dialog.open = True
            page.update()
            
        alert_dialog = ft.CupertinoAlertDialog(
        content=ft.Text("Are you sure to exit?"),
        actions=[
            ft.CupertinoDialogAction(
                "OK",
                is_destructive_action=False,
                on_click=self.exit_app
            ),
            ft.CupertinoDialogAction(
                text="Cancel", 
                is_destructive_action=True, 
                on_click=close_dialog),
        ],
    )
            
        app_bar = ft.AppBar(
            leading=ft.IconButton(ft.icons.ACCOUNT_BALANCE, on_click=self.go_home, tooltip="Home"),
            leading_width=40,
            title = ft.Text('Tosi Sopiva Laskutus'),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=self.change_theme, tooltip="Change theme"),
                ft.IconButton(ft.icons.EXIT_TO_APP, on_click=open_dialog, tooltip="Exit"),
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
