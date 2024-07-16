from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import yaml
from dotenv import load_dotenv
import sys
import os

# Load environment variables
load_dotenv()

def parse_yaml(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Failed to read the YML file: {e}")
        sys.exit(1)

def main():

    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_yml_file>")
        sys.exit(1)

    path_to_yml_file = sys.argv[1]

    # Check if the file exists and is a file
    if not os.path.isfile(path_to_yml_file):
        print(f"The file {path_to_yml_file} does not exist.")
        sys.exit(1)

    # Read YML query from file
    yaml_data = parse_yaml(path_to_yml_file)
    
    name = yaml_data['name']
    query_id = yaml_data['query_id']
    params_list = yaml_data['params']


    params = []
    for param in params_list:
        for param_name, details in param.items():
            param_type = details[0]['type']
            value = details[1]['value']
            method = getattr(QueryParameter, param_type, None)
            if method:
                params.append(method(name=param_name, value=value))
            else:
                raise ValueError(f"No method found for parameter type '{param_type}'")

    query = QueryBase(
        name=name,
        query_id=query_id,
        params=params,
    )

    print("Results available at", query.url())

    dune = DuneClient.from_env()
    results_df = dune.run_query_dataframe(query)

    data_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)  

    file_name = path_to_yml_file.split('/')[-1].split('.')[0]
    csv_filename = os.path.join(data_folder_path, f'addresses_{file_name}.csv')

    results_df['address'].to_csv(csv_filename, index=False)

    print(f"CSV file has been created: {csv_filename}")

if __name__ == "__main__":
    main()
