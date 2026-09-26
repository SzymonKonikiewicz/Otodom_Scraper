import json
import pandas as pd

def transform_data():
    with open("surowe_dane.json", "r", encoding="utf-8") as f:
        dane = json.load(f)

    try:
        # Dynamicznie pobieramy pierwszy klucz wewnątrz 'data' 
        # (niezależnie czy to 'searchAdsRandomPromoted' czy inna paczka)
        klucz_wyszukiwania = list(dane['data'].keys())[0]
        ogloszenia = dane['data'][klucz_wyszukiwania]['items']
    except (KeyError, IndexError, AttributeError):
        print("❌ Błąd struktury JSON. Sprawdź, czy plik nie jest pusty.")
        return

    wyciagniete_dane = []

    for o in ogloszenia:
        # Bezpieczne wyciąganie czystych kwot (omijanie waluty "PLN")
        cena_calkowita = o.get('totalPrice')
        cena_calkowita_wartosc = cena_calkowita.get('value') if isinstance(cena_calkowita, dict) else None
        
        cena_za_metr = o.get('pricePerSquareMeter')
        cena_za_metr_wartosc = cena_za_metr.get('value') if isinstance(cena_za_metr, dict) else None

        # Wyciąganie nazwy miasta
        lokalizacja = o.get('location', {})
        adres = lokalizacja.get('address', {})
        miasto = adres.get('city', {}).get('name', 'Brak')

        wyciagniete_dane.append({
            'id_ogloszenia': o.get('id'),
            'tytul': o.get('title'),
            'miasto': miasto,
            'typ_transakcji': o.get('transaction'),
            'metraz': o.get('areaInSquareMeters'),
            'liczba_pokoi': o.get('roomsNumber'),
            'pietro': o.get('floorNumber'),
            'cena_calkowita': cena_calkowita_wartosc,
            'cena_za_metr': cena_za_metr_wartosc
        })

    # Tworzenie tabeli
    df = pd.DataFrame(wyciagniete_dane)
    
    # Wyświetlamy nagłówek tabeli w konsoli, żeby zobaczyć efekt
    print(df.head())
    
    # Zapis do pliku CSV
    df.to_csv("czyste_dane.csv", index=False, encoding="utf-8")
    print("\n✅ Gotowe! Zapisano elegancką tabelę do pliku czyste_dane.csv")

if __name__ == "__main__":
    transform_data()