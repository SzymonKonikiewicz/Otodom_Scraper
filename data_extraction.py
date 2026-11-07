import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load api key from .env
load_dotenv()
API_KEY = os.getenv("ZTM_API_KEY")
URL = "https://dane.um.warszawa.pl/api/action/get_bin_utrudnienia_drogowe"


def data_extraction():
    
    headers = {
        "Authorization": f"{API_KEY}"
    }
    
    try:
        response = requests.post(URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Records downloaded -> {len(data)}")
                return data
            if isinstance(data, dict):
                records = data.get("result", [])
                print(f"Records downloaded -> {len(records)}")
                return records
        
        else:
            print("err")
            return []
            
    except Exception as e:
        print(f"errrr {e}")
        return []

def save_to_csv(records, filename="ztm_utrudnienia_raw_data.csv"):
    if not records:
        return

    df = pd.DataFrame(records)
    
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Data saved to -> {filename}")

if __name__ == "__main__":
    raw_data = data_extraction()
    
    if raw_data:
        save_to_csv(raw_data)