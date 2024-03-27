import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
# IMPORT YOU CREATE TABLE 
from db_prod_item import mytable, tb, calldb
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_product_item(page: ft.Page, params: Params, basket: Basket):

	page.scroll = "auto"

	def showInput(e):
		inputcon.offset = transform.Offset(0,0)
		page.update()

	def hidecon(e):
		inputcon.offset = transform.Offset(2,0)
		page.update()

	def savedata(e):
		try:
			# INPUT TO DATABASE
			c = conn.cursor()
			c.execute("INSERT INTO product_item (product_id, sku, qty_in_stock, product_image, price) VALUES(?,?,?,?,?)",(product_id.value, sku.value, qty_in_stock.value, product_image.value, price.value))
			conn.commit()

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE
			page.snack_bar = SnackBar(
				Text("Saved"),)
			page.snack_bar.open = True
   
			product_id.value =''
			sku.value =''
			qty_in_stock.value =''
			product_image.value =''
			price.value =''
   
			# REFRESH TABLE
			tb.rows.clear()
			calldb()
			tb.update()
			page.update()

		except Exception as e:
			print(e)

	# CREATE FIELD FOR INPUT
	product_id = TextField(label="product id")
	sku = TextField(label="sku")
	qty_in_stock = TextField(label="qty in stock")
	product_image = TextField(label="product image")
	price = TextField(label="price")

	# CREATE MODAL INPUT FOR ADD NEW DATA 
	inputcon = Card(
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=30,
		content=Container(
			content=Column([
				Row([
				Text("Add new item",size=20,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					]),
				product_id,
				sku,
                qty_in_stock,
                product_image,
                price,    
				FilledButton("Save",
				on_click=savedata)
			])
		)
	)

	return ft.View(
    	"/page_product_item",
     	scroll = "always",
        
       	controls=[
            AppBar().build(),
            Text("PRODUCT ITEM",size=30,weight="bold"),
			ElevatedButton("add new item", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/page_cabinet')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )