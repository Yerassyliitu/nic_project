from dotenv import load_dotenv
import os

load_dotenv()

BASE_STEAM_API_URL = os.environ.get("BASE_STEAM_API_URL")
STEAM_API_KEY = os.environ.get("STEAM_API_KEY")