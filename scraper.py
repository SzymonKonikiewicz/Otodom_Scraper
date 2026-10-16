from playwright.sync_api import sync_playwright
import json
import time
import random
import os

def intercept_response(response):
    if "api/query" in response.url:
        try:
            data = response.json()
            
            if not data.get("errors") and data.get("data"):
                
                if "totalPrice" in str(data):
                    
                    with open("surowe_dane.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        
                    print(f"✅ JSON saved")
        except Exception:
            pass

def run_scraper():
    print("Browser launch")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.on("response", intercept_response)
        
        base_search_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa"
        
        for page_num in range(1, 6): 

            if page_num == 1:
                current_url = base_search_url
            else:
                current_url = f"{base_search_url}?page={page_num}"
                
            print(f"Entering page number {page_num}")
            
            page.goto(current_url, wait_until="networkidle")
            
            delay = random.uniform(3, 8)
            print(f"{delay:.1f} delay")
            time.sleep(delay)
            
        print("Task finished. Closing the browser.")
        browser.close()

if __name__ == "__main__":
    run_scraper()