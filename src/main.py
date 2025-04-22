import flet as ft


def main(page: ft.Page):
    page.title = "Attendance App"
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    txt = ft.Text(value = "Good Day. Please be on Time!!", size = 50)
    txt_name = ft.TextField(label = "Name", width = 300 )
    txt_dept = ft.TextField(label = "Department", width = 300)
    txt_time = ft.TextField(label = "Time", read_only = True, width = 300)
    txt_date = ft.TextField(label = "Date", read_only = True, width = 300)
    

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
        txt_dept,
        txt_time,
        txt_date,
        btn_clock,
    )


ft.app(main)
