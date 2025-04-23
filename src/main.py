import flet as ft
from datetime import datetime
import time
import gspread




def main(page: ft.Page):
    page.title = "Attendance App"
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Gspread API CONNECTION
    service_acc = gspread.service_account(filename='C:/Users/crenz/Documents/GitHub/Attendance-App/src/credentials.json')
    key = service_acc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")
    worksheet = key.sheet1

    # LOCAL VARIABLE
    txt = ft.Text(value = "Good Day. Please be on Time!!", size = 50)
    txt_name = ft.TextField(label = "Name", width = 300)
    name_dropdown = ft.Dropdown(label = "Select your name", width = 300, visible = False)
    '''name_dropdown = ft.Dropdown(
        label = "Name",
        width = 300,
        options = [
            ft.dropdown.Option("Jett"),
            ft.dropdown.Option("Skye"),
            ft.dropdown.Option("Reyna"),
        ]
    )'''

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
    cur_date = datetime.now().strftime("%Y-%m-%d")
    cur_time = datetime.now().strftime("%H:%M:%S")
    txt_time = ft.Text("")  
    txt_date = ft.Text("")
            
        
    def get_all_names():
        names = worksheet.col_values(1)[1:]  # Skip header row
        unique_names = []
        for name in names:
            name = name.strip()
            unique_names.append(name)
        option_list = []
        for name in unique_names:
            option_list.append(ft.dropdown.Option(name))
        return option_list
    name_dropdown.options = get_all_names()

    # FUNCTION TO GET THE NEXT EMPTY ROW in COLUMN A1(1st COLUMN)
    def get_next_empty_cell():
        col = worksheet.col_values(1)
        next_empty_row = len(col) + 1
        return next_empty_row



    # ALERT DIALOG SHOWN AFTER A SUCCESFUL CLOCK-IN, CLOCK-OUT AND WARNING WHEN FIELD ARE EMPTY
    def clock_out_btn(e):
        page.close(dlg_clock_out)    

    dlg_clock_out = ft.AlertDialog(
        modal = True,
        title = ft.Text("Have a nice day Worker"),
        content = ft.Text("You've Succesfully Clock-out"),
        actions = [
            ft.TextButton("Confirm", on_click = clock_out_btn),
        ]
    )

    def clock_in_btn(e):
        page.close(dlg_clock_in)

    dlg_clock_in = ft.AlertDialog(
        modal = True,
        title = ft.Text("Good Day Worker"),
        content = ft.Text("You've Succesfully Clock-in"),
        actions = [
            ft.TextButton("Confirm", on_click = clock_in_btn),
        ]
    )

    def warn_btn(e):
        page.close(dlg_alert)
    dlg_alert = ft.AlertDialog(
        title=ft.Text("Warning!"),
        content=ft.Text("Field cannot be empty. Please fill in the details."),
        actions=[
            ft.TextButton("OK", on_click = warn_btn)
        ],
    )

    # FUNCTION TO RECIRD ATTENDANCE TO GOOGLE SHEET
    def clock_in(e):
        if txt_name.value.strip() or name_dropdown.value and dept_dropdown.value:
            name = txt_name.value
            dept = dept_dropdown.value
            if cur_time >= "18:01:00":
                timeout = cur_time
                status = "Out"
                page.open(dlg_clock_out)
            
            elif cur_time >= "09:00:00":
                timeout = "Pending" 
                status = "In"
                next_empty_cell = get_next_empty_cell()
                worksheet.update(range_name = f"A{next_empty_cell}:F{next_empty_cell}" , values=[[name,dept,cur_time,timeout,status,cur_date]])
                page.open(dlg_clock_in)
                
        else:
            page.open(dlg_alert)


    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click = clock_in,
        width = 200,
        height = 40, 
    )

    page.add(
        txt,
        txt_name,
        name_dropdown,
        dept_dropdown,
        run_date,
        run_time,
        btn_clock,
    )

    # FUNCTION TO SHOW REAL-TIME SYSTEM CLOCK AND UPDATE BUTTON BASED ON TIME
    while True:
        run_date.value = f"Date:  {cur_date}"
        run_time.value = f"Time: {cur_time}"
        
        if cur_time >= "18:01:00":
            btn_clock.text = "Time-Out"
            txt_name.visible = False
            name_dropdown.visible = True
    
        elif cur_time >= "09:00:00":
            txt_name.visible = True
            name_dropdown.visible = False

        page.update()
        time.sleep(1)

ft.app(main)
