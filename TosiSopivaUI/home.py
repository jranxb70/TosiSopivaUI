import flet as ft
from flet_route import Params, Basket
from flet import *

def Home(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/",
        
       controls=[
            AppBar(title=Text('TosiSopivaLaskutus'), bgcolor='blue'),
            Text(value='TosiSopivaLaskutus', size=30),
            ElevatedButton(text='Registration', on_click=lambda _:page.go('/page_reg'))
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )