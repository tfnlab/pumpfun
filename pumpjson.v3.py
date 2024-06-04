import pandas as pd
import requests
import time

def save_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"CSV file saved: {filename}")
    except Exception as e:
        print(f"Error occurred while saving CSV: {e}")

def fetch_data():
    base_url = "https://client-api-2-74b1891ee9f9.herokuapp.com/coins"
    offset = 0
    limit = 50
    data_map = {}

    while len(data_map) < 100:  # Fetch only up to the latest 300 records
        url = f"{base_url}?offset={offset}&limit={limit}&sort=created_timestamp&order=DESC&includeNsfw=true"
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            json_data = response.json()
            if not json_data:
                break

            for item in json_data:
                mint = item.get("mint")
                if mint not in data_map:
                    data_map[mint] = item
                else:
                    print(f"Duplicate mint found: {mint}")

            offset += limit
        else:
            print("Error: Failed to fetch data from the URL")
            break

    return pd.DataFrame(data_map.values())

def main():
    csv_filename = "tokendata/coin_data.latest.csv"
    
    new_df = fetch_data()
    
    # Sort by created_timestamp in descending order and keep only the latest 300 records
    new_df = new_df.sort_values(by='created_timestamp', ascending=False).head(300)

    save_csv(new_df, csv_filename)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
