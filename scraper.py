from playwright.sync_api import sync_playwright
import json

def intercept_response(response):
    # Wyłapujemy dokładnie to zapytanie GraphQL, które namierzyłeś
    if "api/query" in response.url and "GetRandomAudiencePlusAds" in response.url:
        if response.status == 200:
            try:
                data = response.json()
                with open("surowe_dane.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("✅ Sukces! Przechwycono i zapisano JSON z ogłoszeniami!")
            except Exception as e:
                print(f"Błąd podczas parsowania JSON: {e}")

def run_scraper():
    with sync_playwright() as p:
        # headless=False otwiera fizyczne okno przeglądarki, żebyś widział co się dzieje
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Podpinamy funkcję nasłuchującą
        page.on("response", intercept_response)
        
        print("🚀 Uruchamianie przeglądarki i ładowanie strony...")
        # Docelowy link do wyszukiwarki (Warszawa, mieszkania na sprzedaż)
        search_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa"
        
        page.goto(search_url, wait_until="networkidle")
        browser.close()

if __name__ == "__main__":
    run_scraper()