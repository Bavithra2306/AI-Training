import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

PRIMARY_MODEL = "openai/gpt-oss-20b:free"
FALLBACK_MODEL = "nvidia/nemotron-nano-9b-v2:free"