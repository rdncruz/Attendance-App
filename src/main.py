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
    txt_name = ft.TextField(label = "Name", width = 300)
    txt_dept = ft.TextField(label = "Department", width = 300)    

    # FUNCTION TO GET THE NEXT EMPTY ROW in COLUMN A1(1st COLUMN)
    #def get_next_empty_cell():
        #col = worksheet.col_values(1)
        #next_empty_row = len(col) + 1
        #return next_empty_row

    # ALERT DIALOG SHOWN AFTER A SUCCESFUL CLOCK-IN, CLOCK-OUT AND WARNING WHEN FIELD ARE EMPTY
      
    # FUNCTION TO RECIRD ATTENDANCE TO GOOGLE SHEET
    def clock_in(e):
        cur_date = datetime.now().strftime("%Y-%m-%d")
        cur_time = datetime.now().strftime("%H:%M:%S") 
        name = txt_name.value
        dept = txt_dept.value 
        if cur_time >= "18:01:00":
            status = "Out"
            #next_empty_cell = get_next_empty_cell()
            #worksheet.update(range_name = f"A{next_empty_cell}:E{next_empty_cell}" , values=[[name,dept,cur_time,status,cur_date]])
            worksheet.update(range_name = f"A2:E2" , values=[[name,dept,cur_time,status,cur_date]])
        

        elif cur_time >= "09:00:00":
                status = "In"
                #next_empty_cell = get_next_empty_cell()
                worksheet.update(range_name = f"A2:E2" , values=[[name,dept,cur_time,status,cur_date]])
            
       

    btn_clock = ft.ElevatedButton(
        "Time in",
        on_click = clock_in,
        width = 200,
        height = 40, 
    )

    page.add(
        txt_name,
        txt_dept,
        btn_clock,
    )

    # FUNCTION TO SHOW REAL-TIME SYSTEM CLOCK AND UPDATE BUTTON BASED ON TIME
    while True:

        real_time = datetime.now().strftime("%H:%M:%S")  

        if real_time >= "18:01:00":
            btn_clock.text = "Time-Out"
            txt_name.visible = False

        elif real_time >= "09:00:00":
            btn_clock.text = "Time-In"
            
        page.update()
        time.sleep(1)

ft.app(main)
