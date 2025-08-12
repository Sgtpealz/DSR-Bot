import requests
import os

def upload_simc_to_wowaudit(simc_data: str) -> bool:
    """Uploads SimC data to WowAudit."""
    WOWAUDIT_API_KEY = os.getenv('WOWAUDIT_API_KEY')
    WOWAUDIT_BASE_URL = os.getenv('WOWAUDIT_BASE_URL')

    headers = {
        "Authorization": f"Bearer {WOWAUDIT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{WOWAUDIT_BASE_URL}/wishlists", headers=headers, json=simc_data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error uploading to WowAudit: {e}")
        return False
