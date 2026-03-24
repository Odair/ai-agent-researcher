import os
from dotenv import load_dotenv

load_dotenv()

SEARCHCANS_API_KEY = os.getenv("SEARCHCANS_API_KEY", "")
SEARCHCANS_BASE_URL = "https://www.searchcans.com/api"
