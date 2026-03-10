import requests
import os
import pandas as pd
from datetime import timedelta
from dotenv import load_dotenv
from forecast import get_direct_solar_forecast

# Lade Umgebungsvariablen aus einer .env Datei, aus Sicherheitsgründen.
load_dotenv()
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
SENSOR_NEXT_HOUR = os.getenv("SENSOR_NEXT_HOUR")
SENSOR_ENTITY = os.getenv("SENSOR_NEXT_HOUR")

# Setze die Parameter der PVA für die Prognose
lat = 47.1660
lon = 8.3969
dec = 35
az = -12
kwp = 6.5

def get_ha_data(SENSOR_NEXT_HOUR):
    # Holt die Prognosedaten von der Home Assistant API.
    url = f"{HA_URL}{SENSOR_NEXT_HOUR}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Fehler bei der API-Abfrage: {e}")
        return None

def get_ha_forecast(entity_id):
    """
    Fragt den Forecast über den Home Assistant Service 'get_forecast' ab.
    Dies ist notwendig, da die Daten nicht mehr in den Attributen stehen.
    """
    # WICHTIG: Service-Calls nutzen den /services/ Endpunkt und POST
    url = f"{HA_URL}/api/services/forecast_solar/get_forecast"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    data = {"entity_id": entity_id}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Die Struktur der Antwort ist: { "entity_id": { "forecast": [...] } }
        result = response.json()
        return result.get(entity_id, {}).get('forecast', [])
    except Exception as e:
        print(f"Fehler beim Abrufen des Services: {e}")
        return None

def find_best_time(forecast_json, duration_hours=2):
    # Berechnet das Zeitfenster mit dem höchsten Ertrag.
    # Extrahiere die stündlichen Daten aus den Attributen
    forecast_list = forecast_json.get('attributes', {}).get('forecast', [])
    
    if not forecast_list:
        print("Keine Forecast-Daten gefunden.")
        return None

    # Daten in ein Pandas DataFrame umwandeln
    df = pd.DataFrame(forecast_list)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Sliding Window: Summiere die Werte über Anzahl Stunden
    # 'rolling' schaut sich immer die Fenster der angegebenen Stunden an
    df['rolling_sum'] = df['production'].rolling(window=duration_hours).sum()

    # Finde den Zeitpunkt mit der maximalen Summe
    best_slot_end = df['rolling_sum'].idxmax()
    
    # Da rolling(2) am Ende des Fensters markiert, ziehen wir die Dauer ab
    best_start_time = best_slot_end - timedelta(hours=duration_hours - 1)
    
    return best_start_time


if __name__ == "__main__":
    if not HA_TOKEN or not HA_URL:
        print("Fehler: Konfiguration in .env unvollständig!")
    else:
        print(f"Standard Parameter: LAT={lat}, LON={lon}, DEC={dec}, AZ={az}, KWP={kwp}")
        auswahl = input("Möchten Sie die Standardwerte verwenden? (j/n): ").lower()

        if auswahl == 'n':
            print("\nBitte geben Sie die neuen Werte ein (Enter für Standardwert):")
            # Falls der User nur Enter drückt, behalten wir den Standardwert bei (or lat)
            lat = input(f"Breitengrad [{lat}]: ") or lat
            lon = input(f"Längengrad [{lon}]: ") or lon
            dec = input(f"Neigung (0-90) [{dec}]: ") or dec
            az = input(f"Ausrichtung (-180 bis 180) [{az}]: ") or az
            kwp = input(f"Leistung in kWp [{kwp}]: ") or kwp
            print("Temporäre Werte übernommen.\n")
            print(f"Verwende: LAT={lat}, LON={lon}, DEC={dec}, AZ={az}, KWP={kwp}")
        else:
            print("Standardwerte werden verwendet.\n")
        print(f"Rufe Prognose von forecast.solar ab...")
        forecast_data = get_direct_solar_forecast(lat, lon, dec, az, kwp)
        
        if forecast_data:
            print(f"Erfolgreich {len(forecast_data)} Datenpunkte empfangen.")
            
            # Berechnung für 2 Stunden Laufzeit
            best_start = find_best_time(forecast_data, duration_hours=2)
            
            if best_start:
                print(f"--- ERGEBNIS ---")
                print(f"Beste Startzeit: {best_start.strftime('%d.%m.%Y um %H:%M')} Uhr")
                print(f"----------------")
        else:
            print("Konnte keine Forecast-Liste extrahieren.")