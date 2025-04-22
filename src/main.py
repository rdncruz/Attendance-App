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
    txt_time = ft.Text("")  
    txt_date = ft.Text("")
    
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
        title = ft.Text("Please Confirm LOG Data"),
        content = ft.Column([]),
        actions = [
            ft.TextButton("Confirm", on_click = confirm_btn),
        ]
    )

    def open_modal(e):
        name = txt_name.value
        dept = dept_dropdown.value
        cur_date = datetime.now().strftime("%Y-%m-%d")
        txt_date.value = f"Time in: {cur_date}"

        cur_time = datetime.now().strftime("%H:%M:%S")
        txt_time.value = f"Time in: {cur_time}"

        if cur_time >= "18:01:00":
            status = "Time-Out"
        else:
            status = "Time-In"

        dlg_modal.content.controls = [
            ft.Text(f"Name: {name}"),
            ft.Text(f"Department: {dept}"),
            txt_date,
            txt_time,
            ft.Text(f"Status: {status}"),
        ]
        page.open(dlg_modal)

    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click = open_modal,
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
        
        if current_time >= "18:01:00":
            btn_clock.text = "Time-Out"
        elif current_time >= "00:01:00":
            btn_clock.text = "Time-in"

        page.update()
        time.sleep(1)


ft.app(main)
