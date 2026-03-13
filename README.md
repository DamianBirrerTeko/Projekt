# Solar-Forecast & Load-Shifting Optimizer

## Nötige Anpassungen
- Für die Übertragung der ermittelten Zeit muss im Home Assistant ein "Zeitpunkt-Eingabe" Helfer erstellt werden.
- Die .env Datei muss lokal erstellt werden. Es sind Infos zur HA Verbindung sowie der PVA enthalten. Siehe .env.example. 
  - Angaben zum Home Assistant:
    - HA_URL: Muss die IP Adresse der HA Installation beinhalten.
    - HA_TOKEN: Muss das im HA erstellte Zugangstoken enthalten.
    - HA_HELPER: Muss die ID des erstellten Helpers enthalten.
  - Angaben zur PVA:
    - lat: Breitegrad der PVA
    - lon: Längengrad der PVA
    - dec: Neigungswinkel der PVA$
    - az: Azimuth der PVA (180° bis -180°)
    - kwp: Die Peakleistung der PVA in kW 
- Die Angaben zur PVA sind optional. Wenn keine Angaben in der .env stehen werden die Standard Werte verwendet.
- Die PVA Angaben können auch bei der Ausführung temporär angepasst werden.

## Übersicht
### 1. Gewähltes Thema
Entwicklung eines Python-basierten Dienstes zur Optimierung des Eigenverbrauchs von
Photovoltaikanlagen durch intelligente Steuerung von Haushaltsgeräten via Home
Assistant.

### 2. Kurze Problemstellung
PV-Anlagen liefern unregelmäßig Energie. Ohne intelligente Steuerung werden
Großverbraucher oft dann genutzt, wenn nicht genügend solarer Ertrag vorhanden ist,
was teuren Netzbezug zur Folge hat. Bestehende Standard-Automatisierungen sind oft
zu starr und berücksichtigen keine Prognosedaten.

### 3. User Stories & Feature
- User Story 1: Als PV-Besitzer möchte ich, dass meine Spülmaschine automatisch im sonnigsten Zeitfenster des Tages läuft, um Stromkosten zu sparen.
- User Story 2: Als Administrator möchte ich die PVA-Parameter (Neigung, Ausrichtung) temporär überschreiben können, um zu simulieren, wie sich eine Erweiterung meiner Anlage auf die Startzeit-Vorschläge auswirken würde.
- User Story 3: Als Home Assistant User möchte ich, dass der ermittelte Startwert an Home Assistant übermittelt wird, damit der Ideale Startzeitpunkt für HA Automationen verwendet werden kann. 
- Feature A: API-Anbindung an Home Assistant zur Abfrage von Forecast-Daten.
- Feature B: Python-Algorithmus zur Identifikation des optimalen Zeitfensters (Peak-
Suche).
- Feature C: Automatisierte Schaltung von Entitäten (Smart Plugs) über die HA-REST-
API.

### 4. Meilenstein- und Paketplanung
1. Setup der Entwicklungsumgebung und API-Konnektivität.
2. Entwicklung des Kern-Algorithmus in Python.
3. Integration in Home Assistant & Dashboard-Erstellung.
4. Finales Testing und Dokumentation.
