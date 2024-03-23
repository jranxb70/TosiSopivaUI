import flet as ft
from flet_route import Params, Basket
import sqlite3
from flet import *
from views.app_bar import AppBar

def page_auth(page: ft.Page, params: Params, basket: Basket):
        
    def auth_user(e):
        db = sqlite3.connect('invoice.db')
        cur = db.cursor()

        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'")
        if cur.fetchone() != None:
            page.snack_bar = ft.SnackBar(ft.Text('Successful login!'))
            page.snack_bar.open = True
            page.go('/page_cabinet')
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Wrong login or password!'))
            page.snack_bar.open = True
            page.update()
        db.commit()
        db.close()

    def validate(e):
        if all([user_login.value, user_pass.value]):   
            btn_auth.disabled = False
        else:
            btn_auth.disabled = True
        page.update() 

    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_pass = ft.TextField(label='Pass', password=True, width=200, on_change=validate)
    btn_auth = ft.OutlinedButton(text='Login', width=200, on_click=auth_user, disabled=True)

    return ft.View(
        "/page_auth",
        
        controls = [
            AppBar().build(),
            Text(value='Login', size=30),
            ft.Row(
              [
                ft.Column(
                  [
                    ft.Text('Login'),
                    user_login,
                    user_pass,
                    btn_auth,
                  ],horizontal_alignment=CrossAxisAlignment.CENTER,
                )
              ],
              alignment=ft.MainAxisAlignment.CENTER
            )
          ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=26
    ) 