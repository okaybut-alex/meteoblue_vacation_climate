import os
from dotenv import load_dotenv

# .env Datei laden (liegt im Projekt-Root)
load_dotenv()

METEOBLUE_API_KEY = os.getenv("METEOBLUE_API_KEY")

if not METEOBLUE_API_KEY:
    raise RuntimeError("METEOBLUE_API_KEY is not set. Add it to .env")