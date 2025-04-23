import gspread
from gspread_formatting import (
    set_data_validation_for_cell_range,
    DataValidationRule,
    BooleanCondition
)

gc = gspread.service_account(filename='../src/credentials.json')

sh = gc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")

ws = sh.sheet1

rule = DataValidationRule(
    condition=BooleanCondition('NUMBER_GREATER', ['10']),
    inputMessage='Value must be greater than 10',
    
    strict=True,
    showCustomUi=True
)
ws.update_acell('A1', '5')
#set_data_validation_for_cell_range(ws, 'A1', rule)


#value_to_insert = 5  # Example value

# Check if the value is greater than 1
#if value_to_insert > 10:
    #ws.update(range_name='A1', values=[[value_to_insert]])
    #print(f'Value {value_to_insert} successfully inserted into A1.')
#else:
    #print('Error: Value must be greater than 10.')
