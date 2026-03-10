from datetime import datetime
from forecast import get_direct_solar_forecast

lat = 47.2345
lon = 8.5678
dec = 35
az = 0
kwp = 10.5

print(f"Test-Parameter: LAT={lat}, LON={lon}, KWP={kwp}")
    
# Funktion aufrufen
data = get_direct_solar_forecast(lat, lon, dec, az, kwp)

if data is not None:
    print(f"ERFOLG: {len(data)} Datenpunkte empfangen.")
    
    # Den ersten und letzten Datenpunkt zur Kontrolle ausgeben
    print(f"Erster Datenpunkt: {data[0]}")
    print(f"Letzter Datenpunkt: {data[-1]}")
    jetzt_str = datetime.now().strftime("%Y-%m-%d %H")
        
    aktuelle_prod = None
    for point in data:
        # Wir prüfen, ob der Zeitstempel mit der aktuellen Stunde beginnt
        if point['datetime'].startswith(jetzt_str):
            aktuelle_prod = point['production']
            zeitpunkt = point['datetime']
            break
    
    if aktuelle_prod is not None:
        print(f"PROGNOSE AKTUELL ({zeitpunkt}): {aktuelle_prod} Wh")
    else:
        # Falls die aktuelle Stunde nicht drin ist (z.B. nachts), nimm den ersten Punkt
        print(f"Info: Keine Daten für die aktuelle Stunde. Nächster Wert: {data[0]['production']} Wh um {data[0]['datetime']}")


    # Validierung der Struktur
    if "datetime" in data[0] and "production" in data[0]:
        print("STRUKTUR-CHECK: Bestanden (Keys 'datetime' und 'production' vorhanden).")
    else:
        print("STRUKTUR-CHECK: Fehlgeschlagen (Keys fehlen).")
else:
    print("FEHLER: Keine Daten empfangen. Prüfe API-URL und Internetverbindung.")