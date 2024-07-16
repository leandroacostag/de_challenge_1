import load_dotenv
import os

# Read the .env file
load_dotenv.load_dotenv()

bitso_api_url = os.getenv("BITSO_API_URL", None)
bitso_api_key = os.getenv("BITSO_API_KEY", None)
bitso_api_secret = os.getenv("BITSO_API_SECRET", None)
logs_level = os.getenv("LOGS_LEVEL", "INFO")
