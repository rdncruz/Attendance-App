import gspread
from datetime import datetime

gc = gspread.service_account(filename='../src/credentials.json')

sh = gc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")



worksheet = sh.sheet1

def find_row_by_name(name):
    try:
        cell = worksheet.find(name)  # Find the cell with the exact name
        row = cell.row  # Retrieve the row number where the name is located
        return row
    except gspread.exceptions.CellNotFound:
        return None  # Return None if the name is not found

# Test the function
name_to_search = "Renz"
row = find_row_by_name(name_to_search)
if row:
    print(f"Name found in row: {row}")
else:
    print("Name not found")


#set_data_validation_for_cell_range(ws, 'A1', rule)


#value_to_insert = 5  # Example value

# Check if the value is greater than 1
#if value_to_insert > 10:
    #ws.update(range_name='A1', values=[[value_to_insert]])
    #print(f'Value {value_to_insert} successfully inserted into A1.')
#else:
    #print('Error: Value must be greater than 10.')
