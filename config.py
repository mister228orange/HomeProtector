LOG_DIR = "/home/USER/bluetooth_logs"
MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"

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
