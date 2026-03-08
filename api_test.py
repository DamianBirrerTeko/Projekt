import os
import requests
from dotenv import load_dotenv

# Lädt die Variablen aus der .env (siehe .env.example) Datei in das System
load_dotenv()
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

#Kann durch eine andere Entity ID ersetzt werden, um einen anderen Sensor abzufragen
ENTITY_ID = "sensor.zd_power_switch_tv_leistung" 

headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}

def test_ha_api():
    try:
        # Anfrage an den spezifischen Sensor senden
        response = requests.get(HA_URL + ENTITY_ID, headers=headers)
        
        # Prüfen, ob die Anfrage erfolgreich war (Status Code 200)
        if response.status_code == 200:
            data = response.json()
            state = data.get('state')
            unit = data.get('attributes', {}).get('unit_of_measurement', '')
            
            print(f"Erfolg! Der Wert von {ENTITY_ID} ist: {state} {unit}")
        else:
            print(f"Fehler beim Abrufen: Status Code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    test_ha_api()