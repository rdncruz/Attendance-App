import flet as ft
from datetime import datetime
import time
import gspread

def main(page: ft.Page):
    page.title = "Attendance App"
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #Gspread API CONNECTION
    service_acc = gspread.service_account(filename='C:/Users/crenz/Documents/GitHub/Attendance-App/src/credentials.json')
    key = service_acc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")
    worksheet = key.sheet1

    #LOCAL VARIABLE
    txt = ft.Text(value = "Good Day. Please be on Time!!", size = 50)
    name_dropdown = ft.Dropdown(
        label = "Name",
        width = 300,
        options = [
            ft.dropdown.Option("Jett"),
            ft.dropdown.Option("Skye"),
            ft.dropdown.Option("Reyna"),
        ]
    )

    dept_dropdown = ft.Dropdown(
        label = "Department",
        width = 300,
        options = [
            ft.dropdown.Option("Web Dev"),
            ft.dropdown.Option("Data Analyst"),
            ft.dropdown.Option("QA Tester"),
        ]
    )
    run_date = ft.TextField(label = "Date", read_only = True, width = 300)
    run_time = ft.TextField(label = "Time", read_only = True, width = 300)
    txt_time = ft.Text("")  
    txt_date = ft.Text("")

    #FUNCTION TO GET THE NEXT EMPTY ROW in COLUMN A1(1st COLUMN)
    def get_next_empty_cell():
        col = worksheet.col_values(1)
        next_empty_row = len(col) + 1
        return next_empty_row


    def confirm_btn(e):
        page.close(dlg_modal)

    dlg_modal = ft.AlertDialog(
        modal = True,
        title = ft.Text("Good Day Worker"),
        content = ft.Text("You've Succesfully Clock-in"),
        actions = [
            ft.TextButton("Confirm", on_click = confirm_btn),
        ]
    )
    
    #FUNCTION TO RECIRD ATTENDANCE TO GOOGLE SHEET
    def clock_in(e):
        name = name_dropdown.value
        dept = dept_dropdown.value
        cur_date = datetime.now().strftime("%Y-%m-%d")
        cur_time = datetime.now().strftime("%H:%M:%S")

        if cur_time >= "18:01:00":
            timeout = cur_time()
            status = "Out"
        elif cur_time >= "09:00:00":
            timeout = "Pending" 
            status = "In"

        '''dlg_modal.content.controls = [
            ft.Text(f"Name: {name}"),
            ft.Text(f"Department: {dept}"),
            txt_date,
            txt_time,
            #ft.Text(f"Status: {status}"),
        ]'''
        next_empty_cell = get_next_empty_cell()

        worksheet.update(range_name = f"A{next_empty_cell}:F{next_empty_cell}" , values=[[name,dept,cur_time,timeout,status,cur_date]])
        page.open(dlg_modal)

    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click = clock_in,
        width = 200,
        height = 40, 
    )

    page.add(
        txt,
        name_dropdown,
        dept_dropdown,
        run_date,
        run_time,
        btn_clock,
    )

    #FUNCTION TO SHOW REAL-TIME SYSTEM CLOCK AND UPDATE BUTTON BASED ON TIME
    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        run_date.value = f"Date:  {current_date}"
        run_time.value = f"Time: {current_time}"
        
        if current_time >= "18:01:00":
            btn_clock.text = "Time-Out"
        #elif current_time >= "10:25:00":
            #btn_clock.disabled = True
        elif current_time >= "09:00:00":
            btn_clock.text = "Time-in"

        page.update()
        time.sleep(1)

ft.app(main)
