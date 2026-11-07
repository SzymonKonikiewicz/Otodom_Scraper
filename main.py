from data_extraction import data_extraction, save_to_csv
from data_loader import data_loader
from data_transformation import data_transformation

if __name__ == "__main__":

    raw_data = data_extraction()

    if raw_data:
        save_to_csv(raw_data)

        transformed_data = data_transformation("ztm_utrudnienia_raw_data.csv")

        if transformed_data is not None and not transformed_data.empty:
            data_loader()