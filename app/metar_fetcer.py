
import requests
import xml.etree.ElementTree as ET

def fetch_metar(icao):
    url = "https://aviationweather.gov/adds/dataserver_current/httpparam"
    params = {
        "dataSource": "metars",
        "requestType": "retrieve",
        "format": "xml",
        "stationString": icao,
        "hoursBeforeNow": 1,
        "mostRecent": "true"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: Unable to fetch METAR data (status code {response.status_code})"

    root = ET.fromstring(response.content)
    metar = root.find(".//raw_text")

    if metar is not None and metar.text:
        return metar.text
    else:
        return f"No METAR data found for {icao}"
