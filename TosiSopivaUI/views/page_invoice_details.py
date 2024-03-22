import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
from db_invoices import bill
from Bill import generate_bill

import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)


def page_invoice_details(page: ft.Page, params: Params, basket: Basket):        
    
    return ft.View(
    	"/page_invoice_details",
        
       	controls=[
        	AppBar().build(),
            Text("INVOICE",size=30,weight="bold"),
            bill,
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/page_all_invoices')),
            ElevatedButton(text='Download PDF', on_click=generate_bill),
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )