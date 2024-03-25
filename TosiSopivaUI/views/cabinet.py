import flet as ft
from flet_route import Params, Basket
from flet import *
from views.app_bar import AppBar

def page_cabinet(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/page_cabinet",
        
       controls=[
            AppBar().build(),
            Text("Cabinet",size=30,weight="bold"),
            ElevatedButton(text='Customers', on_click=lambda _:page.go('/page_all_customers')),
            ElevatedButton(text='Products', on_click=lambda _:page.go('/page_all_products')),
            ElevatedButton(text='Products Categories', on_click=lambda _:page.go('/page_product_category')),
            ElevatedButton(text='Companies', on_click=lambda _:page.go('/page_all_companies')),
            ElevatedButton(text='Invoices', on_click=lambda _:page.go('/page_all_invoices')),
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )