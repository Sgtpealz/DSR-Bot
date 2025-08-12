import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WOWAUDIT_API_KEY")
base_url = os.getenv("WOWAUDIT_BASE_URL")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(f"{base_url}/team", headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
