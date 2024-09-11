import requests
import json
import os

def fetch_third_wave_wallet_info(wallet_addresses):
    url = 'https://api.thirdwavelabs.com/evm/wallets/batch'
    headers = {
        'X-Api-Key': os.environ.get("THIRDWAVE_API_KEY"),
        'Content-Type': 'application/json'
    }
    data = json.dumps(wallet_addresses)
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()['data']  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching wallet info: {e}")
        return None