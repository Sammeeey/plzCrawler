#! python3
#plzMaker.py - Script to run plzcrawler.py (to add zip codes to address table)

from plzCrawler import AddressFinder

# Input query for table data:
print(f"""\nPlease tell me the name of your address table.
It must contain the columns "Name", "Street", "ZIP", "City".
and it must be an .xlsx document
Excel-Name:""")
ExcelName = input()

print(f"""\nPlease tell me the name of the spreadsheet within your address table
spreadsheetname:""")
spreadsheetname = input()

print(f"""\nPlease tell me the path to the folder in which your table is located.
The path must be specified in Windows format - e.g. 'C:\\Users\\Username\\Documents'
Pfad:""")
addressofexcelfile = input()

print(f"""\nDANGER!:
If a table with the name '{ExcelName}+zip code' exists in the specified folder, it will be overwritten.
If you want to avoid this, please move this table to another folder first!
Do you agree that the table '{ExcelName}+zip code' may be overwritten? [y/n]""")
confirmation = input()

crawl = None
if confirmation != 'y':
    crawl = False
else:
    crawl = True

while not crawl:
    print(f"""\nExecution of the program was aborted.
You can always start the program again when you are ready.""")
    break
else:
    try:
        f = AddressFinder(ExcelName, spreadsheetname, addressofexcelfile)
        openn = f.openAddressTable()
        extract1, extract2, extract3 = f.getColumnLists(openn)
        
        find1, find2 = f.searchAddress(extract2, extract3)

        df = f.makePlzDataframe()




        f.savePlzTable(df)

        print(f"\nYou can find their table including postcodes in the following directory\n"
              f">>> '{f.tableDirectoryRawString}'\n"
              f"The table bears the name '{f.excelTableNameString}+PLZ'")

    except FileNotFoundError as fnfError:
        print('\nThe following error has occurred:\n'
              + str(fnfError.__class__.__name__) + '\n'
            '----------\n'
            'Apparently the specified file or path could not be found.\n'
            'The program will now exit without making any changes.\n'
            'You can restart the program execution to enter the correct data.\n', end=2 * '\n')

    except ImportError as impError:
        print('\nThe following error occurred:\n'
              + str(impError.__class__.__name__) + '\n'
            '----------\n'
            'An incorrect name was probably specified for the spreadsheet.\n'
            'The program will now exit without making any changes.\n'
            'You can restart the program execution to enter the correct data.\n', end=2 * '\n')
