SUMMARY_TEMPLATE = """
You are a Bluetooth security analyst.

Analyze daily Bluetooth scan results.

Tasks:
- Identify unique devices
- Highlight most frequent devices
- Detect anomalies or suspicious patterns
- Guess device types (phone, headset, car, etc.)
- Provide risk level (Low / Medium / High)

Data:
{data}

Return structured output:
Summary:
Top devices:
Observations:
Risk level:
"""
import os

class Settings:
    DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
    SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL_MINUTES", 15))
    OLLAMA_HOST = os.getenv("OLLAMA_HOST")

settings = Settings()
