import pandas as pd
import sys
import os
from dotenv import load_dotenv
from flipside import Flipside

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_sql_file>")
        sys.exit(1)

    path_to_sql_file = sys.argv[1]

    # Check if the file exists and is a file
    if not os.path.isfile(path_to_sql_file):
        print(f"The file {path_to_sql_file} does not exist.")
        sys.exit(1)

    # Read SQL query from file
    try:
        with open(path_to_sql_file, 'r') as file:
            sql_query = file.read()
    except Exception as e:
        print(f"Failed to read the SQL file: {e}")
        sys.exit(1)

    # Load api key
    FLIPSIDE_API_KEY = os.getenv('FLIPSIDE_API_KEY')
    if not FLIPSIDE_API_KEY:
        print("FLIPSIDE_API_KEY is not set in the .env file.")
        sys.exit(1)


    url = "https://api-v2.flipsidecrypto.xyz"
    flipside = Flipside(FLIPSIDE_API_KEY, url)
    query_result_set = flipside.query(sql_query)

    
    # Path to the parent directory's data folder
    data_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data_update')
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)  

    file_name = path_to_sql_file.split('/')[-1].split('.')[0]
    csv_filename = os.path.join(data_folder_path, f'addresses_{file_name}.csv')

    df = pd.DataFrame(query_result_set.rows, columns=query_result_set.columns)
    df['address'].to_csv(csv_filename, index=False)

    print(f"CSV file has been created: {csv_filename}")


if __name__ == "__main__":
    main()


