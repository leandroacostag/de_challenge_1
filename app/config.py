import load_dotenv
import os

# Read the .env file
load_dotenv.load_dotenv()

bitso_api_url = os.getenv("BITSO_API_URL", None)
logs_level = os.getenv("LOGS_LEVEL", "INFO")
data_path = os.getenv("DATA_PATH", "../data")
