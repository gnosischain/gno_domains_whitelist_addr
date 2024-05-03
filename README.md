# .gno Domains Whitelisted Addresses

This repository houses a suite of scripts designed to compile a list of whitelisted addresses for the launch of .gno domains. It targets holders of GNO as of '2024-05-02' who maintain a non-zero balance, while specifically excluding addresses associated with centralized and decentralized exchanges. The scope covers both the Ethereum and Gnosis Chain networks. Additionally, the collection includes Gnosis validators with '01' withdrawal credentials up to slot 15140211, encompassing all validators whether active, exited, or otherwise. The scripts responsible for these operations are organized in the scripts folder and work with data managed within the data and sql_queries folders.

## Directory Structure

- **`/scripts`**: Contains all executable Python scripts.
  - `validators_at_slot.py`: Retrieves validator withdrawal credentials for a specified slot and converts them to ETH1 addresses.
  - `flipsidecrypto_query.py`: Executes SQL queries stored in `/sql_queries` to fetch addresses of GNO holders on both the Ethereum and Gnosis chains.
  - `merge_csvs.py`: Merges multiple CSV files into a single file, eliminating duplicate entries.
- **`/data`**: Used to store CSV files and outputs from scripts.
- **`/sql_queries`**: Contains SQL query files used by the `flipsidecrypto_query.py` script.

## Script Details

### `validators_at_slot.py`

This script extracts validator withdrawal credentials for a given blockchain slot and converts these credentials into ETH1 addresses. It requires the slot number as an input parameter.

#### Usage:
```bash
python scripts/validators_at_slot.py <slot_number>
```


### `flipsidecrypto_query.py`

Executes pre-defined SQL queries from the /sql_queries folder. These queries are designed to retrieve addresses of GNO token holders across both the Ethereum and Gnosis blockchains.

#### Usage:
```bash
python scripts/flipsidecrypto_query.py <path_to_sql_file>
```

### `merge_csvs.py`

Merges all CSV files starting with addresses_ located in the /data folder into a single file, removing duplicates in the process. The result is saved as final_addresses.csv in the same folder.

#### Usage:
```bash
python scripts/merge_csvs.py
```

## Getting Started

To get started with this repository, clone it to your local machine and ensure you have Python and Pandas installed. You can install the required packages using:

```bash
pip install -r requirements.txt
```

Note: Ensure your .env file is properly configured as per the scripts' requirements for environment variables such as API keys and URL endpoints.