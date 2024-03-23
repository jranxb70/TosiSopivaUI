import flet as ft
from flet_route import Params, Basket
from validate_email import validate_email
import sqlite3
from flet import * 
from views.app_bar import AppBar   

def page_reg(page: ft.Page, params: Params, basket: Basket):
    
    def register(e):
        db = sqlite3.connect('invoice.db')
        
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT,
            email TEXT
        )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}', '{user_email.value}')")
        db.commit()
        db.close()
        if validate_email(user_email.value) == True:
          page.snack_bar = ft.SnackBar(ft.Text('Registered!'))
          page.snack_bar.open = True
          page.go('/page_auth')
        else:
          page.snack_bar = ft.SnackBar(ft.Text('Wrong email format!'))
          page.snack_bar.open = True
          page.update()      

    def validate(e):
        if all([user_login.value, user_pass.value, user_email.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()
   
    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_pass = ft.TextField(label='Pass', password=True, width=200, on_change=validate)
    user_email = ft.TextField(label='Email', width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Sign in', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Login', width=200, on_click=lambda _:page.go('/page_auth'), disabled=True)
    btn_change = ft.ElevatedButton(text='Click me!', width=200, on_click=lambda _:page.go('/page_auth'))
    reg_field = ft.Text('Already registered?',width=200,  text_align=ft.TextAlign.CENTER)
    return ft.View(
        "/page_reg",
        
        controls = [
            AppBar().build(),
            Text(value='Registration', size=30),
            ft.Row(
              [
                ft.Column(
                  [
                    ft.Text('Sign in'),
                    user_login,
                    user_pass,
                    user_email,
                    btn_reg,
                    reg_field,
                    btn_change
                  ],
                )
              ],
              alignment=ft.MainAxisAlignment.CENTER
            )
          ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=26
    ) 