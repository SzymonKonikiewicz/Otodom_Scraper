import requests

## python env name -> etl_env


API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJYWmlSemFKTmhKMy1GZ3RDSkdtT1FxQnAzR0pZME44b2N1b3I5MGZOVzQwIiwiaWF0IjoxNzk0MDY1OTc3fQ.XKmZWGZLKAGlkMKS_mQBCcgF6CFcYBtjrp2JnA8lFDI"
URL = "https://dane.um.warszawa.pl/api/action/get_bin_utrudnienia_drogowe"

# ZTM Warszawa najczęściej przyjmuje token jako parametr 'apikey' w URL lub nagłówku
headers = {
    "Authorization": f"{API_KEY}" # albo po prostu sam klucz, zależnie od dokumentacji endpointu
}

# Niektóre endpointy ZTM wolą klucz wprost w adresie URL, np.:
# URL_Z_KLUCZEM = f"{URL}?apikey={API_KEY}"

response = requests.post(URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Sukces! Pobrano dane:")
    print(data)
else:
    print(f"Błąd: {response.status_code}", response.text)