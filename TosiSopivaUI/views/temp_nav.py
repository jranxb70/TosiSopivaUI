import flet as ft
from flet_route import Params, Basket
from flet import *

def temp_nav(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/temp_nav",
        
       controls=[
            AppBar(title=Text('Temp NAv bar'), bgcolor='blue'),
            ElevatedButton(text='Clients', on_click=lambda _:page.go('/page_all_clients')),
            ElevatedButton(text='Products', on_click=lambda _:page.go('/page_all_products')),
            ElevatedButton(text='Invoices', on_click=lambda _:page.go('/page_all_invoices')),
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )