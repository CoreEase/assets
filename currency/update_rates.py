import json
import requests
from pathlib import Path
import sys

CURRENCY_INFO_PATH = Path("currency/currency.json")
SOURCES = [
    "https://currency-api.pages.dev/v1/currencies/usd.json",
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json",
    "https://cdn.moneyconvert.net/api/latest.json"
]
OUTPUT_FILE = "currency/final_rates.json"

try:
    with open(CURRENCY_INFO_PATH, 'r', encoding='utf-8') as f:
        currency_data = json.load(f)
    print(f"Loaded {len(currency_data)} currencies from {CURRENCY_INFO_PATH}")
except FileNotFoundError:
    print(f"Error: {CURRENCY_INFO_PATH} not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing {CURRENCY_INFO_PATH}: {e}")
    sys.exit(1)

def fetch_rates(source_url):
    try:
        print(f"Fetching from: {source_url}")
        response = requests.get(source_url, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"Successfully fetched from {source_url}")
        return data
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
    sys.exit(1)

print(f"Successfully fetched from {len(rates_sources)} sources")

combined_rates = {}
source_used = {}

for idx, source_data in enumerate(rates_sources):
    source_name = SOURCES[idx]
    rates = None
    
    if "usd" in source_data and isinstance(source_data["usd"], dict):
        rates = source_data["usd"]
    elif "rates" in source_data and isinstance(source_data["rates"], dict):
        rates = source_data["rates"]
    
    if not rates:
        print(f"No rates found in source: {source_name}")
        continue
    
    print(f"Processing {len(rates)} rates from {source_name}")
    
    for code, rate in rates.items():
        if code not in combined_rates and code in currency_data:
            combined_rates[code] = rate
            source_used[code] = source_name

print(f"Combined {len(combined_rates)} matching currencies")

if not combined_rates:
    print("No matching currencies found. Check that currency codes match between sources.")
    print(f"Sample codes from currency_data: {list(currency_data.keys())[:5]}")
    if rates_sources:
        sample_rates = list(rates_sources[0].get("usd", rates_sources[0].get("rates", {})).keys())[:5]
        print(f"Sample codes from API: {sample_rates}")
    sys.exit(1)

final_data = {}
for code, rate in combined_rates.items():
    final_data[code] = currency_data[code].copy()
    final_data[code]["rate"] = rate
    if "decimal_digits" in final_data[code]:
        try:
            final_data[code]["rate"] = round(rate, final_data[code]["decimal_digits"])
        except:
            pass

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Successfully created: {OUTPUT_FILE}")
print(f"Total fiat currencies included: {len(final_data)}")
print(f"Sample currencies: {list(final_data.keys())[:5]}")

missing_currencies = set(currency_data.keys()) - set(combined_rates.keys())
if missing_currencies:
    print(f"Warning: {len(missing_currencies)} currencies from currency_data not found in API rates")
