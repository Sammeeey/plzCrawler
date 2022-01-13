#! python3
#plzMaker.py - Skript zur Ausführung von plzcrawler.py (zur Ergänzung von Postleitzahlen in Adresstabelle)

from plzCrawler import AddressFinder

# Input-Abfrage für Tabellendaten:
print(f"""\nBitte nennen Sie mir den Namen Ihrer Adressentabelle.
Sie muss die Spalten "Name", "Straße", "PLZ", "Stadt" enthalten
und es muss sich um ein .xlsx-Dokument handeln
Tabellen-Name:""")
tabellenName = input()

print(f"""\nBitte nennen Sie mir den Namen des Tabellenblattes innerhalb Ihrer Adresstabelle
Tabellenblatt:""")
tabellenBlatt = input()

print(f"""\nBitte nennen Sie mir den Pfad, zu dem Ordner in dem sich Ihre Tabelle befindet.
Der Pfad muss im Windows-Format angegeben werden - z.B. 'C:\\Users\\Username\\Documents'
Pfad:""")
tabellenPfad = input()

print(f"""\nACHTUNG!:
Falls eine Tabelle mit dem Namen '{tabellenName}+PLZ' im angegebenen Ordner existiert wird diese überschrieben.
Sofern Sie dies vermeiden möchten, verschieben Sie diese Tabelle vorab bitte in einen anderen Ordner!
Sind Sie damit einverstanden, dass die Tabelle '{tabellenName}+PLZ' ggf. überschrieben wird? [j/n]""")
confirmation = input()

crawl = None
if confirmation != 'j':
    crawl = False
else:
    crawl = True

while not crawl:
    print(f"""\nDie Ausführung des Programms wurde abgebrochen.
Sie können das Programm jederzeit wieder starten, sobald Sie bereit sind.""")
    break
else:
    try:
        f = AddressFinder(tabellenName, tabellenBlatt, tabellenPfad)
        #f = AddressFinder('Adressen für Herr Hartmann stark gekürzt', 'Addressen', r'C:\Users\Samuel\Documents\Business\WebCrawling Freelancing\Kunden WebCrawling Automatisierung\Nils Henkel Excel PLZ Crawler')
        openn = f.openAddressTable()
        extract1, extract2, extract3 = f.getColumnLists(openn)
        #print(extract1)
        #print(len(extract1))
        #print(extract2)

        #print(len(extract2))

        find1, find2 = f.searchAddress(extract2, extract3)
        #print(f'Hier ist Ihre namenListe, Sir:\n{f.namenListe}\nMit der Länge {len(f.namenListe)}', end='\n')
        #print(f'Hier ist Ihre strassenListe, Sir:\n{f.strassenListe}\nMit der Länge {len(f.strassenListe)}', end='\n')
        #print(f'Hier ist Ihre PLZ-Liste, Sir:\n{f.plzListe}\nMit der Länge {len(f.plzListe)}', end='\n')
        #print(f'Hier ist Ihre placePlzListe, Sir:\n{f.placePlzListe}\nMit der Länge {len(f.placePlzListe)}', end='\n')

        df = f.makePlzDataframe()




        f.savePlzTable(df)

        print(f"\nIhre Tabelle inklusive Postleitzahlen finden Sie im folgenden Verzeichnis\n"
              f">>> '{f.tableDirectoryRawString}'\n"
              f"Die Tabelle trägt den Namen '{f.excelTableNameString}+PLZ'")

    except FileNotFoundError as fnfError:
        print('\nEs ist der folgende Error aufgetreten:\n'
              + str(fnfError.__class__.__name__) + '\n'
            '----------\n'
            'Die angegebene Datei oder der Pfad konnten offenbar nicht gefunden werden.\n'
            'Das Programm wird jetzt beendet, ohne dass Änderungen vorgenommen werden.\n'
            'Sie können die Ausführung des Programms erneut starten, um die korrekten Daten einzugeben.\n', end=2 * '\n')

    except ImportError as impError:
        print('\nEs ist der folgende Error aufgetreten:\n'
              + str(impError.__class__.__name__) + '\n'
            '----------\n'
            'Wahrscheinlich wurde ein falscher Name für das Tabellenblatt angegeben.\n'
            'Das Programm wird jetzt beendet, ohne dass Änderungen vorgenommen werden.\n'
            'Sie können die Ausführung des Programms erneut starten, um die korrekten Daten einzugeben.\n', end=2 * '\n')