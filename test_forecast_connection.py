from forecast import get_direct_solar_forecast

def test_forecast_connection():
    # Wir nutzen Test-Koordinaten
    lat, lon, dec, az, kwp = 52.52, 13.40, 35, 0, 5
    
    # Ausführung
    result = get_direct_solar_forecast(lat, lon, dec, az, kwp)
    
    # Überprüfungen
    assert result is not None, "Die API hat gar keine Daten geliefert."
    assert isinstance(result, list), "Das Ergebnis sollte eine Liste von Dictionaries sein."