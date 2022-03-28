# plzCrawler
Python command line tool which finds topographical addresses based on spreadsheet data and adds postal codes automatically

Version Date: 2021-07-01

pace: approximately 1 second/row

![Before and After image that shows functionality of this github project](https://github.com/Sammeeey/plzCrawler/blob/main/example_images/BeforeAfterSpreadsheet.png?raw=true)

## Live Usage (Sample Application)
https://user-images.githubusercontent.com/49591562/149321073-ea311b45-3d7a-4d35-bcc9-80df0c651c82.mp4

## Installation & Execution (English 🇺🇸 🇬🇧 Windows 10)

### Installation & Preparation

1.  <span style="font-family: Calibri, sans-serif;">if necessary, install Python on the PC if you have not already done so</span>

2.  <span style="font-family: Calibri, sans-serif;">(If necessary, prepare an Excel sheet according to the general conditions - if not already done)</span>

    1.  <span style="font-family: Calibri, sans-serif;">.xlsx-Format</span>

    2.  <span style="font-family: Calibri, sans-serif;">Table columns: name, street (Format: _<span style="font-weight: normal;">street name house number</span>_,ZIP (empty), city</span>

### <span style="font-family: Calibri, sans-serif;">Execution</span>

<span style="font-family: Calibri, sans-serif;">_Note: While the program is working best do not open any of the tables_</span>

##### <span style="font-family: Calibri, sans-serif;">Navigate to software files</span>

1.  <span style="font-family: Calibri, sans-serif;">Open "Command Prompt" (CMD).</span>

    1.  <span style="font-family: Calibri, sans-serif;">Press Windows key + R > type "cmd" > press Enter</span>

2.  <span style="font-family: Calibri, sans-serif;">Navigate in CMD to path where crawler files ("plzCrawler.py" & "plzMaker.py") and the requirements.txt are located</span>
    1. <span style="font-family: Calibri, sans-serif;">Enter text according to the following pattern:  
        cd C:\Users\Username\Documents\plzcrawler</span>

##### <span style="font-family: Calibri, sans-serif;">Create virtual environment (venv).</span>

1.  <span style="font-family: Calibri, sans-serif;">Type the following text in CMD & press Enter (to create a virtual environment named "venv"):
     py -m venv venv</span>
    
##### <span style="font-family: Calibri, sans-serif;">activate venv</span>

1.  <span style="font-family: Calibri, sans-serif;">Type the following text in CMD & press Enter:
     venv\Scripts\activate.bat</span>

##### <span style="font-family: Calibri, sans-serif;">**install requirements.txt in venv**</span>

1.  <span style="font-family: Calibri, sans-serif;">Type the following text in CMD & press Enter:
     pip install -r requirements.txt</span>

##### <span style="font-family: Calibri, sans-serif;">Run the executable file ("plzMaker.py") and follow the instructions</span>

1.  <span style="font-family: Calibri, sans-serif;"><span style="text-decoration: none;">Type the following text in CMD & press Enter:
    </span>py plzMaker.py</span>

##### <span style="font-family: Calibri, sans-serif;">find finished spreadsheet</span>

<span style="font-family: Calibri, sans-serif;">The finished spreadsheet is in the folder of the original spreadsheet.
It can be recognized by the '+PLZ' ending.
The new document looks very similar to the original document and now includes the postcodes found.
It may also contain information as to why individual postcodes could not be found.</span>




