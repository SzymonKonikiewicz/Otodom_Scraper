import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from data_transformation import data_transformation

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def data_loader():
    df = data_transformation()
    
    if df is None or df.empty:
        print("No data to Load")
        return

    print(f"DB connection -> {DB_HOST}:{DB_PORT}...")
    try:
        engine = create_engine(DATABASE_URL)
        
        df.to_sql(
            name='utrudnienia_drogowe',
            con=engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        
    except Exception as e:
        print(f"dasfgsdfag{e}")

if __name__ == "__main__":
    data_loader()