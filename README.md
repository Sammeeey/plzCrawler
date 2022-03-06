# plzCrawler
Python Software that can find topographical addresses based on spreadsheet - to add postal codes automatically

Version Date: 2021-07-01

pace: approximately 1 second/row

![Before and After image that shows functionality of this github project](https://github.com/Sammeeey/plzCrawler/blob/main/example_images/BeforeAfterSpreadsheet.png?raw=true)

## Live Usage (Sample Application)
https://user-images.githubusercontent.com/49591562/149321073-ea311b45-3d7a-4d35-bcc9-80df0c651c82.mp4

## Installation & Ausführung (German🇩🇪 Windows 10)

### <a name="__RefHeading___Toc104_1789371751"></a><span style="font-family: Calibri, sans-serif;">Installation & Vorbereitung</span>

1.  <span style="font-family: Calibri, sans-serif;">ggf. Python auf PC installieren, sofern noch nicht geschehen</span>

2.  <span style="font-family: Calibri, sans-serif;">(ggf. Excelsheet entsprechend Rahmenbedingungen vorbereiten  
    – sofern noch nicht geschehen)</span>

    1.  <span style="font-family: Calibri, sans-serif;">.xlsx-Format</span>

    2.  <span style="font-family: Calibri, sans-serif;">Tabellen-Spalten: Name, Straße (Format: _<span style="font-weight: normal;">Straßenname Hausnummer</span>_, PLZ (leer), Stadt</span>

### <span style="font-family: Calibri, sans-serif;">Ausführung</span>

<span style="font-family: Calibri, sans-serif;">_Hinweis: Während das Programm arbeitet_ _am besten_ _keine der Tabellen öffnen_</span>

##### <span style="font-family: Calibri, sans-serif;">Zu Software-Dateien navigieren</span>

1.  <span style="font-family: Calibri, sans-serif;">"Eingabeaufforderung" (CMD) öffnen</span>

    1.  <span style="font-family: Calibri, sans-serif;">Windows-Taste + R drücken > "cmd" eingeben > Enter drücken</span>

2.  <span style="font-family: Calibri, sans-serif;">In CMD zu Pfad navigieren, in dem sich Crawler-Dateien ("plzCrawler.py" & "plzMaker.py") und das requirements.txt befinden</span>
    1. <span style="font-family: Calibri, sans-serif;">Text nach folgendem Muster eingeben:  
        cd C:\Users\Username\Documents\plzcrawler</span>

##### <span style="font-family: Calibri, sans-serif;">Virtuelle Umgebung (venv) erstellen</span>

1.  <span style="font-family: Calibri, sans-serif;">Folgenden Text in CMD eingeben & Eingabetaste drücken (um virtuelle Umgebung mit dem Namen "venv" zu erstellen):  
    py -m venv venv</span>
    
##### <span style="font-family: Calibri, sans-serif;">venv aktivieren</span>

1.  <span style="font-family: Calibri, sans-serif;">Folgenden Text in CMD eingeben & Eingabetaste drücken:  
    venv\Scripts\activate.bat</span>

##### <span style="font-family: Calibri, sans-serif;">**Requirements.txt in venv installieren**</span>

1.  <span style="font-family: Calibri, sans-serif;">Folgenden Text in CMD eingeben & Eingabetaste drücken:  
    pip install -r requirements.txt</span>

##### <span style="font-family: Calibri, sans-serif;">ausführende Datei ("plzMaker.py") ausführen und Anweisungen folgen</span>

1.  <span style="font-family: Calibri, sans-serif;"><span style="text-decoration: none;">Folgenden Text in CMD eingeben & Eingabetaste drücken:  
    </span>py plzMaker.py</span>

##### <span style="font-family: Calibri, sans-serif;">fertiges Tabellendokument finden</span>

<span style="font-family: Calibri, sans-serif;">Das fertige Tabellendokument befindet sich im Ordner des ursprünglichen Tabellendokumentes.  
Es ist erkennbar an der '+PLZ'-Endung.  
Das neue Dokument sieht dem ursprünglichen Dokument sehr ähnlich und ist nun um die gefundenen Postleitzahlen ergänzt.  
Außerdem enthält es ggf. Hinweise, weshalb einzelne Postleitzahlen nicht gefunden werden konnten.</span>
