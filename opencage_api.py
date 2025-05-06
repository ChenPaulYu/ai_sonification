import requests
from typing import Optional, Tuple

from config import OPENCAGE_API_KEY

def location_text_to_latlon(
    location_text: str,
) -> Optional[Tuple[float, float]]:
    """
    Convert a human-readable location description to latitude and longitude.

    Args:
        location_text (str): e.g., "Taipei 101", "Golden Gate Bridge"
        api_key (str, optional): OpenCage API key. Defaults to OPENCAGE_KEY env var.

    Returns:
        (lat, lon) tuple or None if not found
    """

    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location_text,
        "key": OPENCAGE_API_KEY,
        "limit": 1,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Geocoding failed: {response.status_code}, {response.text}")

    data = response.json()
    if data["results"]:
        geometry = data["results"][0]["geometry"]
        return geometry["lat"], geometry["lng"]
    else:
        return None

if __name__ == "__main__":
    coords = location_text_to_latlon("Taipei 101")
    if coords:
        print(f"📍 Coordinates: {coords}")
    else:
        print("❌ Location not found")