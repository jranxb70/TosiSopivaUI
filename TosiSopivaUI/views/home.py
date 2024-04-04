from flet_route import Params, Basket
from flet import *
from views.app_bar import AppBar

def Home(page: Page, params: Params, basket: Basket):
    imgcontainer = Container(
        content = Image(src="TosiSopivaUI\\img\\bg.jpg", opacity=0.4),
        padding=-10,
        margin=0,
    )
    
    body = Container(
        Stack([
            imgcontainer,
            Column([
                Container(height=400),
                Row([
                    FilledButton("START",
                    style=ButtonStyle(shape=CircleBorder(),padding=30),
                    on_click=lambda _:page.go('/page_reg'),
            ),
            ],alignment=MainAxisAlignment.CENTER,) 
            ]),
        ],)
    )
   
    return View(
        "/",        
       controls=[
            AppBar().build(),
            body
        ],
    )