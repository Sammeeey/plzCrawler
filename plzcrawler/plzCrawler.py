#! python3
#plzcrawler.py - Programm zur Ergänzung von Postleitzahlen in Adresstabelle
# https://nominatim.openstreetmap.org

import requests
import json
from pprint import pprint
import os
import pandas as pd

# Straße & Stadt für alle Zeilen aus .xlsx-Tabelle rauslesen und in Python verfügbar machen
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
        """nimmt Name einer Exceltabelle in Form eines Strings,
        den Namen des entsprechenden Tabellenblattes in Form eines Strings,
        & die Windows-Tabellen-Directory in Form eines Raw-Strings;
        navigiert zum angegebenen Windows-Pfad & öffnet die Tabelle als pandas-dataframe;
        speichert Tabelle als pandas dataframe-object"""

        # zu directory navigieren, die Tabelle enthält
        dir = os.chdir(self.tableDirectoryRawString)
        # print(Path.cwd())

        openedAddressTable = pd.read_excel(open(f'{self.excelTableNameString}.xlsx', 'rb'),
                                          sheet_name=self.workSheetString)
        # print(df)
        return openedAddressTable

    def getColumnLists(self, addressDataframe):
        """nimmt pandas dataframe-object als input-argument;
        holt relevante Spalten aus input-object heraus;
        gibt ausgewählte Spaltenwerte in Listen gleicher Länge aus"""

        # Spalte "Namen" aus Input-Tabelle (dataframe-object) holen
        namen = addressDataframe['Name']
        namenNpArray = namen.values
        self.namenListe = list(namenNpArray)

        # Spalte "Straße" aus Input-Tabelle (dataframe-object) holen
        strassen = addressDataframe['Straße']
        strassenNpArray = strassen.values
        self.strassenListe = list(strassenNpArray)

        # Spalte "Stadt" aus Input-Tabelle (dataframe-object) holen
        stadt = addressDataframe['Stadt']
        stadtNpArray = stadt.values
        self.stadtListe = list(stadtNpArray)

        return self.namenListe, self.strassenListe, self.stadtListe


    #Nominatum Suchanfragen für alle Zeilen durchführen
    #Annahme: Listen gleicher Länge mit Spalten-Daten aus Tabelle
    def searchAddress(self, strassenListe, stadtListe):
        """nimmt Staßennamen & -nummern, sowie Stadtnamen in Form von gleichlangen Listen;
        führt mithilfe des Nominatum-Tools & der einzelnen Strings innerhalb der input-Listen (als Adressen)
        eine Suche in der OpenStreetMap-API durch;
        gibt die Postleitzahlen des jeweils ersten Suchergebnisses
        oder (bei Nicht-Finden) einen Platzhalter ('N/A') in Form einer Liste aus"""

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
                print('Es ist ein '+str(atError.__class__.__name__)+ ' Error aufgetreten.\n'
                      'Wahrscheinlich war der "addesstags"-Eintrag in der API-Anfrage eine leere Liste.\n'
                        'Das heißt die Adresse konnte nicht gefunden werden.', end=2*'\n')
                self.placePlzListe.append('N/A - Adresse unauffindbar')

            except IndexError as inError:
                print('Es ist ein '+str(inError.__class__.__name__)+ ' Error aufgetreten.\n'
                        'Scheinbar wurde kein Karteneintrag für die Adresse gefunden.\n'
                        'Das könnte daran liegen, dass die Adresse ein ungewöhnliches Format hat.', end=2*'\n')
                self.placePlzListe.append('N/A - Adressformat prüfen!')

        return self.placePlzListe, self.placeIdListe
        # placePlzListe aus "Adressen für Herr Hartmann gekürzt.xlsx" Länge = 49:
        # kurzPlzListe = ['47051', '47119', '47249', '47051', '47053', '47228', '47057', '47239', '47057', '44139', '44139', '44135', '44135', 'N/A - Adresse unauffindbar', '44135', 'N/A - Adresse unauffindbar', '44263', '44225', '44263', '42275', '42283', '42275', '42285', '42107', '42283', '42275', '42103', '42103', '42117', '48153', None, None, '48143', '48143', '48151', '48155', '48155', '48155', '48143', '40219', '40477', '40477', '40479', '40219', 'N/A - Adressformat prüfen!', '40210', '40215', '40219', '40233']


# PLZ des ersten Suchergebnisses für jede Zeile in .xlsx-Tabelle ergänzen
    def makePlzDataframe(self):
        """nimmt Spaltendaten (mindestens eine(!), aus urpsrünglicher Tabelle) in Form von Listen;
        konvertiert diese in ein Dictioinary;
        gibt kombinierte Listen mit Spaltennamen in Form eines pandas-dataframe aus"""

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

    # neue Tabelle speichern
    def savePlzTable(self, inputDfName):
        """nimmt pandas-dataframe;
        speichert pandas dataframe unter ursprünglichem Tabellennamen (mit "+PLZ") in Form einer .xlsx-Tabelle"""

        inputDfName.to_excel(f'{self.excelTableNameString}+PLZ.xlsx', sheet_name=self.workSheetString)



#todo: Code bereinigen, verständlich machen & dokumentieren




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