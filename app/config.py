import os
from dotenv import load_dotenv

load_dotenv()

SEARCHCANS_API_KEY = os.getenv("SEARCHCANS_API_KEY", "")
SEARCHCANS_BASE_URL = "https://www.searchcans.com/api"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
# CrewAI default LLM is OpenAI; set a Claude id so only ANTHROPIC_API_KEY is needed.
CREW_LLM_MODEL = os.getenv("CREW_LLM_MODEL", "claude-sonnet-4-20250514")
