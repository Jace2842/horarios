
import requests

def fetch_clima_open_meteo(latitude: float, longitude: float) -> dict:
    """
    Consulta la API de Open-Meteo para obtener datos meteorológicos actuales
    en la latitud/longitud indicadas.

    Devuelve el JSON decodificado por requests.json(), o lanza excepción si hay error.
    """
    api_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        "&forecast_days=1&timeformat=unixtime"
    )

    resp = requests.get(api_url, timeout=5)
    resp.raise_for_status()  # lanza HTTPError si código != 200
    return resp.json()
