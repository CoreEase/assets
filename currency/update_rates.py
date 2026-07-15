import json
import requests
from pathlib import Path

CURRENCY_INFO_PATH = Path("currency/currency.json")
SOURCES = [
    "https://currency-api.pages.dev/v1/currencies/usd.json",
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json",
    "https://cdn.moneyconvert.net/api/latest.json"
]
OUTPUT_FILE = "final_rates.json"

try:
    with open(CURRENCY_INFO_PATH, 'r', encoding='utf-8') as f:
        currency_data = json.load(f)
except FileNotFoundError:
    print(f"Error: {CURRENCY_INFO_PATH} not found.")
    exit()

def fetch_rates(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch from {source_url}: {e}")
        return None

rates_sources = []
for url in SOURCES:
    data = fetch_rates(url)
    if data:
        rates_sources.append(data)

if not rates_sources:
    print("Failed to fetch from all sources.")
    exit()

combined_rates = {}
for source_data in rates_sources:
    if "usd" in source_data:
        rates = source_data["usd"]
    elif "rates" in source_data:
        rates = source_data["rates"]
    else:
        continue

    for code, rate in rates.items():
        if code not in combined_rates and code in currency_data:
            combined_rates[code] = rate

final_data = {}
for code, rate in combined_rates.items():
    if code in currency_data:
        final_data[code] = currency_data[code]
        final_data[code]["rate"] = rate

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Successfully created: {OUTPUT_FILE}")
print(f"Total fiat currencies included: {len(final_data)}")
