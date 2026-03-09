import requests
import os
import pandas as pd
from datetime import timedelta
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus einer .env Datei, aus Sicherheitsgründen.
load_dotenv()
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
SENSOR_NEXT_HOUR = os.getenv("SENSOR_NEXT_HOUR")

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

def analyze_solar_peak(data, duration=2):
    """
    Simpler Algorithmus zur Peak-Suche.
    TODO: In WP 2 (Logic-Layer) verfeinern (Sliding Window mit Pandas).
    """
    # Hier kommt die Logik aus dem Pseudocode rein
    print(f"Analysiere Daten für ein Zeitfenster von {duration} Stunden...")
    pass



if __name__ == "__main__":
    if not HA_TOKEN:
        print("Fehler: Kein HA_TOKEN in der .env gefunden!")
    else:
        forecast_data = get_ha_data(SENSOR_NEXT_HOUR)
        if forecast_data:
            print(f"Daten erfolgreich empfangen: {forecast_data.get('state')} kWh")
            analyze_solar_peak(forecast_data)
            print(f"Beste Startzeit: {find_best_time(forecast_data)}")