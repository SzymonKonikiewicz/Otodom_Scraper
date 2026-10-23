import pandas as pd
import json
import os
import glob

def extract_all_properties(element, collected_list):
    if isinstance(element, dict):
        if "areaInSquareMeters" in element and "title" in element:
            collected_list.append(element)
        
        for value in element.values():
            extract_all_properties(value, collected_list)
            
    elif isinstance(element, list):
        for item in element:
            extract_all_properties(item, collected_list)

def parse_and_clean_data():
    print(f"Current working directory: {os.getcwd()}")
    
    json_files = glob.glob("raw_data_*.json")
    if not json_files:
        print("❌ No raw_data_*.json files found.")
        return

    extracted_properties = []
    print(f"🔍 Found {len(json_files)} files. Vacuuming ALL data...")

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                raw_data = json.load(file)
            except Exception as e:
                print(f"⚠️ Error loading JSON from {file_path}: {e}")
                continue
                
            all_file_properties = []
            extract_all_properties(raw_data, all_file_properties)
            
            if not all_file_properties:
                continue
            
            print(f"✔️ Extracted {len(all_file_properties)} raw items from {file_path}")
            
            # THE FIX: Safely parse each item independently
            for item in all_file_properties:
                try:
                    price_dict = item.get("totalPrice") or {}
                    price = price_dict.get("value") if isinstance(price_dict, dict) else None
                    
                    # Safe location extraction handling 'null' (None) values gracefully
                    location_dict = item.get("location") or {}
                    address_dict = location_dict.get("address") or {}
                    city_dict = address_dict.get("city") or {}
                    district_dict = address_dict.get("district") or {}

                    city = city_dict.get("name", "Unknown")
                    district = district_dict.get("name", "Unknown")

                    extracted_properties.append({
                        "Title": item.get("title", "No Title"),
                        "Price_PLN": price,
                        "Area_sqm": item.get("areaInSquareMeters"),
                        "Rooms": item.get("roomsNumber"),
                        "City": city,
                        "District": district
                    })
                except Exception as e:
                    # If ONE listing is completely broken, skip it and continue with the next
                    continue

    df = pd.DataFrame(extracted_properties)
    
    if df.empty:
        print("Data File is Empty.")
        return

        
    # Remove duplicates
    df = df.drop_duplicates(subset=["Title", "Price_PLN", "Area_sqm"])
    
    # Drop rows without Price or Area
    df = df.dropna(subset=['Price_PLN', 'Area_sqm'])
    
    # Type conversion
    df['Price_PLN'] = df['Price_PLN'].astype(int)
    df['Area_sqm'] = df['Area_sqm'].astype(float)
    
    # Feature engineering: Price per square meter
    df['Price_per_sqm'] = (df['Price_PLN'] / df['Area_sqm']).round(2)

    output_csv_name = "parsed_data.csv"
    df.to_csv(output_csv_name, index=False, encoding="utf-8")
    
    print("Success!")
    print(f"Saved file: {output_csv_name}\n")

if __name__ == "__main__":
    parse_and_clean_data()