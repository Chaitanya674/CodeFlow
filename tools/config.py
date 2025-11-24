import os
from dotenv import load_dotenv
from google.genai import types

# Load .env from the same directory as this config file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
# If using Kaggle secrets UI, this might already be set — otherwise set manually in an ephemeral way.
os.environ["GOOGLE_API_KEY"] = os.getenv("KAGGLE_SECRET_GEMINI_API_KEY")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
CONFLUENCE_API_KEY = os.getenv("CONFLUENCE_API_KEY")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_DOMAIN = os.getenv("CONFLUENCE_DOMAIN")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)