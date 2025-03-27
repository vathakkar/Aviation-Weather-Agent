# app/test_taf.py

import os
from dotenv import load_dotenv
#from app.taf_fetcher import get_taf
from app.notam_fetcher import get_notam

load_dotenv()

icao = "KSEA"
taf = get_notam(icao)
print(taf)
