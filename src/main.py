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
    cur_date = datetime.now().strftime("%Y-%m-%d")
    cur_time = datetime.now().strftime("%H:%M:%S") 
    txt_in = ft.Text(value = "Good Morning, Have Good Day", size = 50)
    txt_out = ft.Text(value = "Good Evening, Good Work", visible = False, size = 50)
    txt_name = ft.TextField(label = "Name", width = 300)
    name_dropdown = ft.Dropdown(label = "Select your name", width = 300, visible = False)
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

    
    #FUNCTION TO GET THE ROW NUMBER BY NAME
    def find_row_by_name(name):
        try:
            cell = worksheet.find(name)  # Find the cell with the exact name
            row = cell.row  # Retrieve the row number where the name is located
            return row
        except gspread.exceptions.CellNotFound:
            return None

    #FUNCTION TO GET ALL THE NAMES (SKIP HEADER ROW)    
    def get_all_names():
        names = worksheet.col_values(1)[1:]
        unique_names = list(dict.fromkeys(name.strip() for name in names if name.strip()))
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
        if txt_name.value.strip() or name_dropdown.value:
            name = txt_name.value
            dept = dept_dropdown.value
            
            if cur_time >= "18:01:00":
                name_to_search = name_dropdown.value
                row = find_row_by_name(name_to_search)
                timeout = cur_time
                status = "Out"
                worksheet.update( range_name=f"D{row}:E{row}", values=[[timeout,status]])  # Update the timeout in column D
                page.open(dlg_clock_out)
            
            elif cur_time >= "09:00:00":
                if dept_dropdown.value:
                    timeout = "Pending" 
                    status = "In"
                    next_empty_cell = get_next_empty_cell()
                    worksheet.update(range_name = f"A{next_empty_cell}:F{next_empty_cell}" , values=[[name,dept,cur_time,timeout,status,cur_date]])
                    page.open(dlg_clock_in)
                else:
                    page.open(dlg_alert)
        else:
            page.open(dlg_alert)

    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click = clock_in,
        width = 200,
        height = 40, 
    )

    page.add(
        txt_in,
        txt_out,
        txt_name,
        name_dropdown,
        dept_dropdown,
        run_date,
        run_time,
        btn_clock,
    )

    # FUNCTION TO SHOW REAL-TIME SYSTEM CLOCK AND UPDATE BUTTON BASED ON TIME
    while True:
        real_date = datetime.now().strftime("%Y-%m-%d")
        real_time = datetime.now().strftime("%H:%M:%S")  
        run_date.value = f"Date:  {real_date}"
        run_time.value = f"Time: {real_time}"
        
        if real_time >= "18:01:00":
            btn_clock.text = "Time-Out"
            txt_in.visible = False
            txt_out.visible =  True
            txt_name.visible = False
            name_dropdown.visible = True
            dept_dropdown.visible = False

        elif real_time >= "09:00:00":
            txt_in.visible = True
            name_dropdown.visible = False
            txt_name.visible = True
            
        page.update()
        time.sleep(1)

ft.app(main)
