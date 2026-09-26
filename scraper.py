from playwright.sync_api import sync_playwright
import json

def intercept_response(response):
    if "api/query" in response.url:
        try:
            data = response.json()
            
            # 1. Ignorujemy puste odpowiedzi i błędy typu PersistedQueryNotFound
            if not data.get("errors") and data.get("data"):
                
                # 2. Upewniamy się, że to JSON z ogłoszeniami (szukamy ceny)
                # Zamieniamy na stringa, żeby szybko przeszukać całą strukturę
                if "totalPrice" in str(data):
                    
                    # 3. Zapisujemy właściwy plik
                    with open("surowe_dane.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        
                    print(f"✅ BINGO! Złapano i zapisano właściwy plik JSON z ofertami z URL: {response.url[:60]}...")
        except Exception:
            pass # Ignorujemy ruch, który nie jest poprawnym JSON-em

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