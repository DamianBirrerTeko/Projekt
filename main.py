import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus einer .env Datei, aus Sicherheitsgründen
load_dotenv()

# Konfiguration
HA_URL = os.getenv("HA_URL", "http://homeassistant.local:8123")
HA_TOKEN = os.getenv("HA_TOKEN")
ENTITY_ID = "sensor.energy_production_forecast_hourly" # Beispiel-Entity

def get_ha_data(entity_id):
    """Holt die Prognosedaten von der Home Assistant API."""
    url = f"{HA_URL}/api/states/{entity_id}"
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
        forecast_data = get_ha_data(ENTITY_ID)
        if forecast_data:
            print(f"Daten erfolgreich empfangen: {forecast_data.get('state')} kWh")
            analyze_solar_peak(forecast_data)