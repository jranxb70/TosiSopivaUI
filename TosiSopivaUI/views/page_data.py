import flet as ft
from flet_route import Params, Basket
from flet import *
from views.app_bar import AppBar

def data(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/page_data",
        
       controls=[
            AppBar().build(),
            Text("DATA",size=30,weight="bold"),
            ElevatedButton(text='Products', on_click=lambda _:page.go('/page_all_products')),
            ElevatedButton(text='Products Categories', on_click=lambda _:page.go('/page_product_category')),
            ElevatedButton(text='Variations', on_click=lambda _:page.go('/page_all_variations')),
            ElevatedButton(text='Variation options', on_click=lambda _:page.go('/page_var_options')),
            ElevatedButton(text='Product items', on_click=lambda _:page.go('/page_product_item')),
            ElevatedButton(text='Back', on_click=lambda _:page.go('/page_cabinet')),
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )