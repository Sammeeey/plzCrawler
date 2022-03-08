#! python3
#plzcrawler.py - Program for adding postal codes to the address table
# https://nominatim.openstreetmap.org

import requests
import json
from pprint import pprint
import os
import pandas as pd

# Read street & city for all rows from .xlsx table and make them available in Python
class AddressFinder:
    def __init__(self, excelTableNameString, workSheetString, tableDirectoryRawString, *args):
        self.workSheetString = workSheetString
        self.excelTableNameString = excelTableNameString
        self.tableDirectoryRawString = tableDirectoryRawString

        self.namenListe = []
        self.strassenListe = []
        self.plzListe = []
        self.stadtListe = []
        self.placePlzListe = []
        self.placeIdListe = []

    def openAddressTable(self):
        # """nimmt Name einer Exceltabelle in Form eines Strings,
        # den Namen des entsprechenden Tabellenblattes in Form eines Strings,
        # & die Windows-Tabellen-Directory in Form eines Raw-Strings;
        # navigiert zum angegebenen Windows-Pfad & öffnet die Tabelle als pandas-dataframe;
        # speichert Tabelle als pandas dataframe-object"""
        '''
        takes the name of an Excel spreadsheet in the form of a string,
        the name of the corresponding spreadsheet in the form of a string,
        & the Windows table directory in the form of a raw string;
        navigate to the specified windows path & open the table as pandas-dataframe;
        saves table as pandas dataframe-object
        '''
        # Navigate to directory containing table
        dir = os.chdir(self.tableDirectoryRawString)
        # print(Path.cwd())

        openedAddressTable = pd.read_excel(open(f'{self.excelTableNameString}.xlsx', 'rb'),
                                        sheet_name=self.workSheetString)
        # print(df)
        return openedAddressTable

    def getColumnLists(self, addressDataframe):
        '''
        takes panda's dataframe object as an input argument;
        pulls relevant columns out of input-object;
        outputs selected column values in lists of equal length
        '''

        # Get column "names" from input table (dataframe-object).
        namen = addressDataframe['Name']
        namenNpArray = namen.values
        self.namenListe = list(namenNpArray)
        
        
        # Get column "Street" from input table (dataframe-object).
        strassen = addressDataframe['Straße']
        strassenNpArray = strassen.values
        self.strassenListe = list(strassenNpArray)
        
        # Get column "City" from input table (dataframe-object).
        stadt = addressDataframe['Stadt']
        stadtNpArray = stadt.values
        self.stadtListe = list(stadtNpArray)

        return self.namenListe, self.strassenListe, self.stadtListe


    #Nominatum Perform searches on all rows
    #Assumption: lists of the same length with column data from table
    def searchAddress(self, strassenListe, stadtListe):
        """
        takes street names & numbers, as well as city names in the form of lists of the same length;
        leads using the nominatum tool & the individual strings within the input lists (as addresses)
        perform a search in the OpenStreetMap API;
        gives the zip code of the first search result
        or (if not found) a placeholder ('N/A') in the form of a list
        """
        #print(f'Straßenliste (Input): {strassenListe}')
        #print(f'Stadtliste (Input): {stadtListe}')

        for i, strasse in enumerate(strassenListe, start=-1):
            print(strasse)
            stadt = stadtListe[i+1]
            print(stadt)

            luckySearch=json.dumps(requests.get(
                f'https://nominatim.openstreetmap.org/search.php?street={strasse}&city={stadt}&country=DE&format=jsonv2').json())

            try:
                luckySearchDic = json.loads(luckySearch)[0] #erster Eintrag in Suchergebnissen
                #pprint(luckySearchDic)
                placeID = luckySearchDic.get('place_id')
                self.placeIdListe.append(placeID)

                placeSearch = json.dumps(requests.get(
                    f'https://nominatim.openstreetmap.org/details.php?place_id={placeID}'
                    f'&addressdetails=1&hierarchy=0&group_hierarchy=1&format=json').json())

                placeSearchDic = json.loads(placeSearch)
                placePlz = placeSearchDic.get('addresstags').get('postcode')
                if placePlz != None:
                    self.placePlzListe.append(placePlz)
                    print(placePlz, end=2*'\n')
                elif placePlz == None:
                    calcPlacePlz = placeSearchDic.get('calculated_postcode')
                    self.placePlzListe.append(calcPlacePlz)
                    print(calcPlacePlz, end=2*'\n')
                else:
                    self.placePlzListe.append('N/A - keine PLZ gefunden')

            except AttributeError as atError:
                print('It is a '+str(atError.__class__.__name__) + ' error occurred.\n'
                    'Most likely the "addesstags" entry in the API request was an empty list.\n'
                    'which means the address could not be found.', end=2*'\n')
                self.placePlzListe.append('N/A - address cannot be found')

            except IndexError as inError:
                print('it is a '+str(inError.__class__.__name__) + ' error occurred.\n'
                        'Apparently no map entry was found for the address.\n'
                        'This could be because the address has an unusual format.', end=2*'\n')
                self.placePlzListe.append('N/A - Check address format!')

        return self.placePlzListe, self.placeIdListe
        # placePlzList from "Addresses for Mr. Hartmann shortened.xlsx" Length = 49:
        # kurzPlzListe = ['47051', '47119', '47249', '47051', '47053', '47228', '47057', '47239', '47057', '44139', '44139', '44135', '44135', 'N/A - address cannot be found', '44135', 'N/A - address cannot be found', '44263', '44225', '44263', '42275', '42283', '42275', '42285', '42107', '42283', '42275', '42103', '42103', '42117', '48153', None, None, '48143', '48143', '48151', '48155', '48155', '48155', '48143', '40219', '40477', '40477', '40479', '40219', 'N/A - Check address format!', '40210', '40215', '40219', '40233']


# Add zip code of first search result for each row in .xlsx table
    def makePlzDataframe(self):
        """takes column data (at least one(!), from original table) in the form of lists;
        converts this to a dictionary;
        outputs combined lists of column names in the form of a pandas dataframe"""
        # # list of name, degree, score
        # firstColumnList = self.namenListe
        # secondColumnList = self.strassenListe
        # thirdColumnList = self.placePlzListe
        # fourthColumnList = self.stadtListe
        # dictionary of lists
        plzDict = {
            'Name': self.namenListe,
            'Straße': self.strassenListe,
            'PLZ': self.placePlzListe,
            'Stadt': self.stadtListe,
        }

        plzDf = pd.DataFrame(plzDict)
        return plzDf

    # save new table
    def savePlzTable(self, inputDfName):
        """takes pandas dataframe;
        saves pandas dataframe under the original table name (with "+zip code") in the form of an .xlsx table"""

        inputDfName.to_excel(f'{self.excelTableNameString}+PLZ.xlsx', sheet_name=self.workSheetString)


#todo: Clean code, make it understandable & document it





# f = AddressFinder()
# openn = f.openAddressTable('Adressen für Herr Hartmann gekürzt', 'Addressen', r'C:\Users\Samuel\Documents\Business\WebCrawling Freelancing\Kunden WebCrawling Automatisierung\Nils Henkel Excel PLZ Crawler')
# extract1, extract2 = f.getColumnLists(openn)
# print(extract1)
# print(len(extract1))
# print(extract2)
# print(len(extract2))
#
# find = f.searchAddress(extract1, extract2)
# print(f'Hier ist Ihre PLZ-Liste, Sir:\n{find}')
# copy(str(find))