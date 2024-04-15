import flet as ft

# def show_alert_dialog():
#     # Create an AlertDialog
#     alert = ft.AlertDialog(
#         title="Important Message",
#         message="This is an alert dialog in Flet.",
#         actions=[
#             ft.DialogAction(text="OK", on_pressed=lambda: print("OK clicked"))
#         ],
#     )

def close_dlg(e):
    dlg_modal.open = False
    #page.update()   
 

dlg_modal = ft.AlertDialog(
    modal=True,
    title=ft.Text("Please confirm"),
    content=ft.Text("Do you really want to delete all those files?"),
    actions=[
        ft.TextButton("Yes", on_click=close_dlg),
        ft.TextButton("No", on_click=close_dlg),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)    

# Show the AlertDialog
#ft.show_dialog(alert)