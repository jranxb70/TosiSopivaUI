import flet as ft
from flet import *
from flet_route import Routing, path
from views.home import Home
from views.page_reg import page_reg
from views.page_auth import page_auth
from views.page_all_customers import page_all_customers
from views.page_all_products import page_all_products
from views.page_all_invoices import page_all_invoices
from views.page_invoice_details import page_invoice_details
from views.page_all_companies import page_all_companies
from views.page_product_category import page_product_category
from views.page_all_variations import page_all_variations
from views.page_var_options import page_var_options
from views.page_product_item import page_product_item
from views.page_invoice_line import page_invoice_line
from views.cabinet import page_cabinet
from views.page_data import data

def main(page: ft.Page):

    app_routes = [
        
        path(url="/", clear= True,view=Home),
        path(url="/page_reg",clear= True, view=page_reg),
        path(url="/page_auth",clear= True, view=page_auth),
        path(url="/page_all_customers",clear= True, view=page_all_customers),
        path(url="/page_all_products",clear= True, view=page_all_products),
        path(url="/page_all_invoices",clear= True, view=page_all_invoices),
        path(url="/page_cabinet",clear= True, view=page_cabinet),
        path(url="/page_invoice_details",clear= True, view=page_invoice_details),
        path(url="/page_all_companies",clear= True, view=page_all_companies),
        path(url="/page_product_category",clear= True, view=page_product_category),
        path(url="/page_all_variations",clear= True, view=page_all_variations),
        path(url="/page_var_options",clear= True, view=page_var_options),
        path(url="/page_product_item",clear= True, view=page_product_item),
        path(url="/page_invoice_line",clear= True, view=page_invoice_line),
        path(url="/page_data",clear= True, view=data),
    ]
    
    Routing(page=page, app_routes=app_routes)
    
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main)