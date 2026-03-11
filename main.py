import os
import pandas as pd
from datetime import timedelta
from dotenv import load_dotenv
from forecast import get_direct_solar_forecast
from send_to_ha import send_to_homeassistant

# Lade Umgebungsvariablen aus der .env Datei.
load_dotenv()

# Setzt Home Assistant Parameter aus der .env Datei
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# Setzt PVA Parameter für die Prognose aus der .env Datei oder verwendet Standardwerte
lat = os.getenv("lat") or 47.1660
lon = os.getenv("lon") or 8.3969
dec = os.getenv("dec") or 35
az = os.getenv("az") or -12
kwp = os.getenv("kwp") or 6.64

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
    
    print(f"Voraussichtliche Energieproduktion in diesem Fenster ({duration_hours}h): {max_energy:.2f} Wh")
    
    return best_start_time

if __name__ == "__main__":

    print(f"\nStandard Parameter: LAT={lat}, LON={lon}, DEC={dec}, AZ={az}, KWP={kwp}")
    auswahl = input("Möchten Sie die Standardwerte verwenden? (j/n): ").lower()

    if auswahl == 'n':
        print("\nBitte geben Sie die neuen Werte ein (Enter für Standardwert):")

        # Falls der User nur Enter drückt, wird der Standardwert behalten (or lat)
        lat = input(f"Breitengrad [{lat}]: ") or lat
        lon = input(f"Längengrad [{lon}]: ") or lon
        dec = input(f"Neigung (0-90) [{dec}]: ") or dec
        az = input(f"Ausrichtung (-180 bis 180) [{az}]: ") or az
        kwp = input(f"Leistung in kWp [{kwp}]: ") or kwp

        # Rückmeldung der übernommenen Werte
        print("Temporäre Werte übernommen.\n")
        print(f"Verwende: LAT={lat}, LON={lon}, DEC={dec}, AZ={az}, KWP={kwp}")

    else:
        print("Standardwerte werden verwendet.\n")

    print(f"Rufe Prognose von forecast.solar ab...")
    forecast_data = get_direct_solar_forecast(lat, lon, dec, az, kwp)
    
    if forecast_data:
        print(f"\nErfolgreich {len(forecast_data)} Datenpunkte empfangen.")
        
        # Berechnung für 2 Stunden Laufzeit
        best_start = find_best_time(forecast_data, duration_hours=2)
        
        if best_start:
            print(f"\n--------------------------- ERGEBNIS ---------------------------")
            print(f"Beste Startzeit: {best_start.strftime("%d.%m.%Y um %H:%M")} Uhr")
            print(f"----------------------------------------------------------------\n")
    
    else:
        print("Konnte keine Forecast-Liste extrahieren.")

    auswahl_ha = input("Möchten Sie das Ergebnis an Home Assistant senden? (j/n): ").lower()

    if not HA_TOKEN or not HA_URL:
        print("\nDie Ergebnisse können nicht an Home Assistant gesendet werden.\nDie .env Daten sind unvollständig!\n")
    
    else:
        if auswahl_ha == 'n':
            print("Ergebnis wird nicht gesendet.")
        else:
            send_to_homeassistant(best_start)