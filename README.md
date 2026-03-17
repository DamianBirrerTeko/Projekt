# Solar-Forecast & Load-Shifting Optimizer

## Nötige Anpassungen
- Installation der benötigten Bibliotheken (z.B. pip install pandas requests python-dotenv)
- Für die Übertragung der ermittelten Zeit muss im Home Assistant ein "Zeitpunkt-Eingabe" Helfer erstellt werden.
- Die .env Datei muss lokal erstellt werden. Es sind Infos zur HA Verbindung sowie der PVA enthalten. Siehe .env.example. 
  - Angaben zum Home Assistant:
    - HA_URL: Muss die IP Adresse der HA Installation beinhalten.
    - HA_TOKEN: Muss das im HA erstellte Zugangstoken enthalten.
    - HA_HELPER: Muss die ID des erstellten Helpers enthalten.
  - Angaben zur PVA:
    - lat: Breitegrad der PVA
    - lon: Längengrad der PVA
    - dec: Neigungswinkel der PVA
    - az: Azimuth der PVA (180° bis -180°)
    - kwp: Die Peakleistung der PVA in kW 
- Die Angaben zur PVA sind optional. Wenn keine Angaben in der .env stehen werden die Standard Werte verwendet.
- Die PVA Angaben können auch bei der Ausführung temporär angepasst werden.

## Funktionsweise
Der Kern des Programms ist ein Predictive Load-Shifting Algorithmus. Anstatt Geräte nur bei aktuellem Sonnenschein zu starten, blickt das Programm in die Zukunft:
1. Datenbeschaffung: Das Skript ruft stündliche Ertragsprognosen direkt von der Forecast.Solar API ab.
2. Zukunfts-Filter: Um Fehlplanungen zu vermeiden, werden alle Prognosewerte, die in der Vergangenheit liegen, sofort gefiltert.
3. Sliding Window Algorithmus: Das Programm legt ein "Fenster" (2 Stunden) über die kommenden 48 Stunden. Es verschiebt dieses Fenster Schritt für Schritt und berechnet die Summe der erwarteten Sonnenenergie in diesem Zeitraum.
4. Peak-Detektion: Der Zeitpunkt mit der höchsten kumulierten Energiemenge wird als optimaler Startzeitpunkt identifiziert.
5. Threshold-Check: Liegt die Energie im besten Fenster unter einem Sicherheits-Schwellenwert (2500 Wh), erfolgt eine Warnung, da sich der Betrieb rein über Solar evtl. nicht lohnt.
