from playwright.sync_api import sync_playwright
import json
import time
import random
import os

file_counter = 1

def intercept_response(response):
    global file_counter
    
    if response.request.resource_type in ["fetch", "xhr"]:
        try:
            data = response.json()
            data_str = str(data)
            
            if "areaInSquareMeters" in data_str and "totalPrice" in data_str:
                file_name = f"raw_data_{file_counter}.json"
                
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
                short_url = response.url.split('?')[0][-40:]
                print(f"✅Captured real estate data: ...{short_url} -> {file_name}")
                
                file_counter += 1
        except Exception:
            pass

def run_scraper():
    print("Browser launch.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.on("response", intercept_response)
        
        search_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa"
        
        print(f"Loading page 1")
        page.goto(search_url)
        
        try:
            page.locator('#onetrust-accept-btn-handler').click(timeout=3000)
            print("🍪Closed cookies banner.")
        except:
            pass

        for target_page in range(2, 6):  
            print("Scrolling...")
            for _ in range(7):
                page.keyboard.press("PageDown")
                time.sleep(0.6)
            next_page_link = page.locator(f"a[href*='page={target_page}']").first
            
            try:
                next_page_link.scroll_into_view_if_needed()
                time.sleep(1) 
                
                next_page_link.click()
                print(f"Clicked page {target_page}")
                time.sleep(random.uniform(4, 6))
                
            except Exception as e:
                print(f"Failed to click page {target_page}. Details: {e}")
                break
            
        print("\n Task finished. Closing the browser.")
        browser.close()

if __name__ == "__main__":
    run_scraper()