import csv
import pandas as pd
import requests
import time

def load_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"CSV file '{filename}' not found.")
        return None

def save_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"CSV file saved: {filename}")
    except Exception as e:
        print(f"Error occurred while saving CSV: {e}")

def main():
    # Load CSV file if it exists
    csv_filename = "tokendata/coin_data.csv"
    existing_df = load_csv(csv_filename)

    base_url = "https://client-api-2-74b1891ee9f9.herokuapp.com/coins"
    offset = 0
    limit = 50
    data_map = {}

    while True:
        url = f"{base_url}?offset={offset}&limit={limit}&sort=created_timestamp&order=DESC&includeNsfw=true"
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            json_data = response.json()
            if not json_data:  # If response is empty, break the loop
                break

            for item in json_data:
                mint = item.get("mint")
                # Check if mint key already exists in existing_df or data_map
                if existing_df is None or mint not in existing_df['mint'].values and mint not in data_map:
                    data_map[mint] = item
                else:
                    print(f"Duplicate mint found: {mint}")

            offset += limit  # Increment offset for the next page
        else:
            print("Error: Failed to fetch data from the URL")
            break

    # Convert data_map to DataFrame
    new_df = pd.DataFrame(data_map.values())

    # If existing_df is None, use new_df as the DataFrame
    if existing_df is None:
        existing_df = new_df
    else:
        # Concatenate existing_df and new_df
        existing_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Save DataFrame to CSV file
    save_csv(existing_df, csv_filename)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(15)