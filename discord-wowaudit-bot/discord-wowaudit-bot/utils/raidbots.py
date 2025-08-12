import re
import requests

def validate_raidbots_link(link: str) -> bool:
    """Validates if the provided link is a valid Raidbots sim report link."""
    pattern = r"^https:\/\/www\.raidbots\.com\/simbot\/report\/[\w]+$"
    return bool(re.match(pattern, link))

def download_simc_input(link: str) -> str | None:
    """Downloads the SimC input.txt from a Raidbots report."""
    try:
        report_id = link.rstrip('/').split('/')[-1]
        input_url = f"https://www.raidbots.com/simbot/report/{report_id}/input.txt"
        response = requests.get(input_url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error downloading simc input: {e}")
        return None
