import requests


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