import pandas as pd

"""
EXAMPLE OF RESPONSE
[
  {
    "start_date": "2025-10-27 08:15:00",
    "end_date": "2025-10-31 04:30:00",
    "content": [
      "W środę, 29 października, rano drogowcy rozpoczną wymianę nawierzchni u zbiegu ulic Pelplińskiej i Sobockiej. Przez dwie doby kierowcy nie przejadą przez remontowane skrzyżowanie.",
      "Drogowcy zamkną remontowane skrzyżowanie w środę, 29 października, o godzinie 6:00. Ulicami Pelplińską i Sobocką ze wszystkich stron będzie można dojechać tylko do miejsca prac.",
      "Przed rozpoczęciem remontu, kierowcy powinni przestawić swoje samochody. W sąsiedztwie skrzyżowana staną znaki zakazujące parkowania wraz z tabliczką informującą o możliwości odholowania pojazdu na koszt właściciela.",
      "Ruch na skrzyżowanie wróci w piątek, 31 października, około godziny 4:00."
    ],
    "name": "Wymienią nawierzchnię na bielańskim skrzyżowaniu",
    "id": 8144,
    "geo": [
      [
        {
          "geomType": 0,
          "latlngs": [
            { "lat": 52.2821269608705, "lng": 20.9699285030365 }
          ]
        }
      ]
    ]
  },
"""

def data_transformation(input_csv="ztm_utrudnienia_raw_data.csv"):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print("File not found")
        return None

    if 'start_date' in df.columns:
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    if 'end_date' in df.columns:
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')

    if 'id' in df.columns:
        df = df.dropna(subset=['id'])
        df['id'] = df['id'].astype(int)

    return df

if __name__ == "__main__":
    transformed_df = data_transformation()
    if transformed_df is not None:
        transformed_df.to_csv("ztm_utrudnienia_transformed.csv", index=False)