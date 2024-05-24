import csv
import json
import requests
import sys

def count_value_occurrences(csv_filename, json_data):
    column_value_counts = {}

    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                if value in json_data.values():
                    mint_key = row.get("mint")
                    if mint_key != json_data.get("mint"):
                        if key not in column_value_counts:
                            column_value_counts[key] = {value: 1}
                        else:
                            if value not in column_value_counts[key]:
                                column_value_counts[key][value] = 1
                            else:
                                column_value_counts[key][value] += 1

    return column_value_counts

def main():
    if len(sys.argv) < 2:
        print("Please provide the coin ID as a command-line argument.")
        return

    print(sys.argv[1])
    url = "https://client-api-2-74b1891ee9f9.herokuapp.com/coins/" + sys.argv[1]
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        csv_filename = "coin_data.csv"
        column_value_counts = count_value_occurrences(csv_filename, json_data)
        
        for column, value_counts in column_value_counts.items():
            print(f"Column: {column}")
            for value, count in value_counts.items():
                print(f"  {value}: {count} times")
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    main()
