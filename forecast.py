import requests
import pandas as pd
from datetime import timedelta

def get_direct_solar_forecast(lat, lon, dec, az, kwp):
    # Holt Forecast-Daten direkt von Forecast.Solar ohne Home Assistant.
    url = f"https://api.forecast.solar/estimate/{lat}/{lon}/{dec}/{az}/{kwp}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Das Feld 'watt_hours_period' enthält die Produktion pro Stunde
        raw_forecast = data.get('result', {}).get('watt_hours_period', {})
        
        # Umwandlung in eine Liste von Dictionaries für Pandas
        formatted_data = []
        for timestamp, production in raw_forecast.items():
            formatted_data.append({
                "datetime": timestamp,
                "production": production
            })
            
        return formatted_data
    except Exception as e:
        print(f"Fehler bei der direkten API-Abfrage: {e}")
        return None

def find_best_time(forecast_list, duration_hours=2):
    # Berechnet den besten Startzeitpunkt basierend auf einer Liste von Prognosedaten.
    if not forecast_list:
        return None

    # Liste in Pandas DataFrame umwandeln
    df = pd.DataFrame(forecast_list)
    
    # Zeitstempel konvertieren und als Index setzen
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Wir nehmen nur Datenpunkte, die mindestens "jetzt" oder später sind
    jetzt = pd.Timestamp.now()
    df = df[df.index >= jetzt]

    # Sliding Window: Summiere die Werte über die Laufzeit
    # window=duration_hours entspricht der Anzahl der Stunden (Zeilen), welche wir summieren wollen
    df['rolling_sum'] = df['production'].rolling(window=duration_hours).sum()

    # Den Slot mit der maximalen Summe finden
    best_slot_end = df['rolling_sum'].idxmax()
    max_energy = df['rolling_sum'].max()
    
    # Da 'rolling' am Ende des Fensters markiert, berechnen wir den Startzeitpunkt
    best_start_time = best_slot_end - timedelta(hours=duration_hours - 1)
    
    if max_energy <= 2500:
        print(f"\nWarnung: Maximale prognostizierte Energieproduktion von {max_energy:.2f} Wh ist sehr niedrig. \nMöglicherweise schlechte Wetterbedingungen oder Fehler in der Prognose.\n")
    else:
        print(f"\nVoraussichtliche Energieproduktion in diesem Fenster ({duration_hours}h): {max_energy:.2f} Wh")
    
    return best_start_time
