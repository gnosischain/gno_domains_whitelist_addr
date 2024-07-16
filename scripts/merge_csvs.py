import pandas as pd
import os
import glob

def main():
    # Path to the parent directory's data folder
    data_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    if not os.path.exists(data_folder_path):
        print("Data folder does not exist.")
        return
    
    pattern = os.path.join(data_folder_path, 'addresses_*.csv')
    
    csv_files = glob.glob(pattern)
    if not csv_files:
        print("No address files found.")
        return
    
    all_addresses = pd.DataFrame()

    for file in csv_files:
        df = pd.read_csv(file)
        all_addresses = pd.concat([all_addresses, df], ignore_index=True)
    
    all_addresses = all_addresses.drop_duplicates().reset_index(drop=True)
    final_file_path = os.path.join(data_folder_path, 'final_addresses.csv')
    all_addresses.to_csv(final_file_path, index=False)
    
    print(f"Final addresses have been saved to: {final_file_path}")

if __name__ == "__main__":
    main()
