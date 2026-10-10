import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("INDIAN_API_KEY")
url     = "https://indianapi.in/stock?name=Reliance"
headers = {"X-Api-Key": API_KEY}

response = requests.get(url, headers=headers)
data     = response.json()

print("=== riskMeter ===")
print(json.dumps(data.get("riskMeter"), indent=2))

print("\n=== keyMetrics ===")
print(json.dumps(data.get("keyMetrics"), indent=2))

print("\n=== stockTechnicalData ===")
print(json.dumps(data.get("stockTechnicalData"), indent=2))

print("\n=== currentPrice ===")
print(json.dumps(data.get("currentPrice"), indent=2))

print("\n=== yearHigh / yearLow ===")
print("yearHigh:", data.get("yearHigh"))
print("yearLow:",  data.get("yearLow"))

