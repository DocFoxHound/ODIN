'''
Will use this file to save code no longer in use just in-case.


        #  Access to worksheet information
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ODIN-bd3fd42186ba.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Items').get_worksheet(0)

        #  return the row and column using input params (spreadsheet)
        sell_station_gen = wks.find(names.facilities.get(value1))
        sell_item_gen = wks.find(names.items.get(value2))
        sell_column_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_station_gen)).split()))
        sell_row_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_item_gen)).split()))
        sell_value_gen = wks.cell(sell_row_gen[0], sell_column_gen[1] + 1).value

'''