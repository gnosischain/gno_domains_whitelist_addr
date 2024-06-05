import requests
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <slot_number>")
        sys.exit(1)

    slot = sys.argv[1]
    base_url = os.getenv('GNOSIS_BEACON_URL')
    if not base_url:
        print("GNOSIS_BEACON_URL is not set in the .env file.")
        sys.exit(1)

    url = f'http://{base_url}/eth/v1/beacon/states/{slot}/validators'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        validators = response.json()['data']

        # Creating a list of dictionaries for each validator
        data = [
            {
                'index': item['index'],
                'status': item['status'],
                'withdrawal_credentials': item['validator']['withdrawal_credentials'],
                'activation_eligibility_epoch': item['validator']['activation_eligibility_epoch'],
                'activation_epoch': item['validator']['activation_epoch'],
                'exit_epoch': item['validator']['exit_epoch'],
            }
            for item in validators
        ]

        df = pd.DataFrame(data)

        # Path to the parent directory's data folder
        data_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data_update')
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)  

        csv_filename = os.path.join(data_folder_path, f'addresses_validators_at_{slot}.csv')

        # Filter out entries with '0x00' 'withdrawal_credentials'
        df = df[~df['withdrawal_credentials'].str.startswith('0x00')]

        # Convert 'withdrawal_credentials' to eth1 address and drop duplicates
        df['address'] = df['withdrawal_credentials'].apply(lambda x: x[:2] + x[-40:])
        df = df.drop_duplicates(subset='address')

        # Write to CSV
        df['address'].to_csv(csv_filename, index=False)

        print(f"CSV file has been created: {csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"JSON decoding failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
