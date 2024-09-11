import requests
import os

def fetch_farcaster_power_users():
    # Replace with the actual API endpoint
    url = 'https://api.neynar.com/v2/farcaster/user/power_lite'
    headers = {
        'accept': 'application/json',
        'api_key': os.environ.get("NEYNAR_API_KEY")  # Replace with your actual API key
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=2)
        results = response.json()['result']["fids"]
        response.raise_for_status()  # Raise an exception for HTTP errors
        return results  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching power users: {e}")
        return None

def fetch_farcaster_user_info(fids):
    # Replace with the actual API endpoint
    url = 'https://api.neynar.com/v2/farcaster/user/bulk'
    params = {
        'fids': ','.join(map(str,fids))
    }
    headers = {
        'accept': 'application/json',
        'api_key': os.environ.get("NEYNAR_API_KEY")  # Replace with your actual API key
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=2)
        results = response.json()['users']
        response.raise_for_status()  # Raise an exception for HTTP errors
        return results  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for FID {fid}: {e}")
        return None