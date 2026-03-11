# Solar-Forecast & Load-Shifting Optimizer

## Nötige Anpassungen
- Die .env Datei muss lokal erstellt werden. Diese Dateien werden für den HA Zugang verwendet. Als Beispiel kann die .env.example verwendet werden.
- Bei Bedarf können die Attribute der Solaranlage im Skript angepasst werden. Wenn dies nich gemacht wird werden die Standard Werte verwendet.

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
- User Story 1: Als PV-Besitzer möchte ich, dass meine Spülmaschine automatisch im
sonnigsten Zeitfenster des Tages läuft, um Stromkosten zu sparen.
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
