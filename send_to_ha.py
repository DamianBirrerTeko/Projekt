import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
HA_HELPER = os.getenv("HA_HELPER")

def send_to_homeassistant(start_time):
    # Übermittelt den Zeitpunkt an den Home Assistant Helfer.
    url = f"{HA_URL}/api/services/input_datetime/set_datetime"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    
    payload = {
        "entity_id": f"{HA_HELPER}",
        "datetime": start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    now = datetime.now()

    # Überprüft ob die Übermittlung erfolgreich war und gibt entsprechende Meldungen aus.
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"\nErfolg: Startzeit wurde um {now.strftime('%d.%m.%Y %H:%M:%S')} an Home Assistant übermittelt.")
            print(f"----------------------------------------------------------------\n")
        else:
            print(f"\nFehler beim Senden: {response.status_code} - {response.text}\n")
    except Exception as e:
        print(f"\nVerbindungsfehler zu Home Assistant: {e}\n")