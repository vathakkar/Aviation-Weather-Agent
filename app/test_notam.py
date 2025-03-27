# app/test_notam.py

from dotenv import load_dotenv
from app.notam_fetcher import get_notams

load_dotenv()

print(get_notams("KRNT"))
