import os
import csv
import requests
import time

# Define the folder containing the CSV files
folder_path = 'tokendata'

# Define the URL for the POST request
url = 'http://localhost:8000/create_token/'

# Function to process a single CSV file
def process_csv(file_path):
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)  # Read all rows into a list
        rows.reverse()       # Reverse the list to start with the last row
        for row in rows:
            # Send a POST request for each row in the CSV
            response = requests.post(url, data=row)
            try:
                response_data = response.json()
            except requests.exceptions.JSONDecodeError:
                response_data = response.text
            
            if response.status_code == 201:
                print(f"Success: {response_data}")
            else:
                print(f"Failed: {response.status_code}, {response_data}")
            
            time.sleep(0.01)

# Continuously process files in the folder
while True:
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            full_path = os.path.join(folder_path, filename)
            process_csv(full_path)
    # Sleep for some time before processing again
    time.sleep(5)  # Adjust this value as needed
