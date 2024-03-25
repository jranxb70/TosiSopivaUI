import flet as ft
from flet import *
from flet_route import Params, Basket
from views.app_bar import AppBar
# IMPORT YOU CREATE TABLE 
from db_products import mytable, tb, calldb
import sqlite3
conn = sqlite3.connect("invoice.db",check_same_thread=False)

def page_all_products(page: ft.Page, params: Params, basket: Basket):

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
			c.execute("INSERT INTO product (category_id,trade_name,product_description) VALUES(?,?,?)",(category_id.value,trade_name.value,product_description.value))
			conn.commit()

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE
			page.snack_bar = SnackBar(
				Text("Saved"),)
			page.snack_bar.open = True
   
			category_id.value =''
			trade_name.value =''
			product_description.value =''
   
			# REFRESH TABLE
			tb.rows.clear()
			calldb()
			tb.update()
			page.update()

		except Exception as e:
			print(e)

	# CREATE FIELD FOR INPUT
	category_id = TextField(label="category id")
	trade_name = TextField(label="trade name")
	product_description = TextField(label="product_description")

	# CREATE MODAL INPUT FOR ADD NEW DATA 
	inputcon = Card(
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=30,
		content=Container(
			content=Column([
				Row([
				Text("Add new product",size=20,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					]),
				category_id,
				trade_name,
				product_description,
				FilledButton("Save",
				on_click=savedata)
			])
		)
	)

	return ft.View(
    	"/page_all_products",
        
       	controls=[
            AppBar().build(),
            Text("PRODUCTS",size=30,weight="bold"),
			ElevatedButton("add new product", on_click=showInput),
   			ElevatedButton(text='Go to Back', on_click=lambda _:page.go('/page_cabinet')),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    )