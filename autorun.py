import os
from dotenv import load_dotenv
from forecast import get_direct_solar_forecast, find_best_time
from send_to_ha import send_to_homeassistant

# Lade Umgebungsvariablen aus der .env Datei.
load_dotenv()

# Setzt Home Assistant Parameter aus der .env Datei
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
HA_HELPER = os.getenv("HA_HELPER")

# Setzt PVA Parameter für die Prognose aus der .env Datei oder verwendet Standardwerte
lat = os.getenv("lat") or 47.1660
lon = os.getenv("lon") or 8.3969
dec = os.getenv("dec") or 35
az = os.getenv("az") or -12
kwp = os.getenv("kwp") or 6.64

# Holt die Prognosedaten für die direkte Sonneneinstrahlung basierend auf den angegebenen Parametern
forecast_data = get_direct_solar_forecast(lat, lon, dec, az, kwp)
    
# Findet die beste Startzeit für die Ladung basierend auf den Prognosedaten und der gewünschten Ladungsdauer (z.B. 2 Stunden)
best_start = find_best_time(forecast_data, duration_hours=2)
        
# Sendet die beste Startzeit an Home Assistant
send_to_homeassistant(best_start)
