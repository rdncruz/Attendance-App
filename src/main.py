import flet as ft
from datetime import datetime
import time

def main(page: ft.Page):
    page.title = "Attendance App"
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    txt = ft.Text(value = "Good Day. Please be on Time!!", size = 50)
    txt_name = ft.TextField(label = "Name", width = 300 )
    run_date = ft.TextField(label = "Date", read_only = True, width = 300)
    run_time = ft.TextField(label = "Time", read_only = True, width = 300)
    
    dept_dropdown = ft.Dropdown(
        label = "Department",
        width = 300,
        options = [
            ft.dropdown.Option("Web Dev"),
            ft.dropdown.Option("Data Analyst"),
            ft.dropdown.Option("QA Tester"),
        ]
    )

    def confirm_btn(e):
        page.close(dlg_modal)

    dlg_modal = ft.AlertDialog(
        modal = True,
        title = ft.Text("Modal is Good"),
        
        actions = [
            ft.TextButton("Confirm", on_click = confirm_btn),
        ]
    )

    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click=lambda e: page.open(dlg_modal),
        width = 200,
        height = 40, 
    )
    page.add(
        txt,
        txt_name,
        dept_dropdown,
        run_date,
        run_time,
        btn_clock,
    )

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        run_date.value = f"Date:  {current_date}"
        run_time.value = f"Time: {current_time}"
        
        page.update()
        time.sleep(1)


ft.app(main)
