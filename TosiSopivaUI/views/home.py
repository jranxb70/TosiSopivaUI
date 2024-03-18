import flet as ft
from flet_route import Params, Basket
from flet import *
from views.app_bar import AppBar

def Home(page: ft.Page, params: Params, basket: Basket):
    reg_button = ft.OutlinedButton(text='Registration', width=200, on_click=lambda _:page.go('/page_reg'))
    title_= ft.Text(value = 'Very Appropriate Billing', size=30)
        
    return ft.View(
        "/",
        
       controls=[
            AppBar().build(),
            title_,
            reg_button,
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )