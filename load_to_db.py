import pandas as pd
from sqlalchemy import create_engine
import os

def load_to_db():
    csv_file="parsed_data.csv"
    try:
        df = pd.read_csv(csv_file, encoding="utf-8")
    except FileNotFoundError:
        return

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "otodom_db")

    engine_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)

    try:
        df.to_sql("warsaw_properties", con=engine, if_exists="replace", index=False)

    except Exception as e:
        print(f"{e}")
        raise e

if __name__ == "__main__":
    load_to_db()


