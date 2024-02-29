# Ethereum Block Crawler

## Overview

The Ethereum Block Crawler is a Python script designed to fetch data for a range of Ethereum blocks via the JSON-RPC endpoint and store this data in a SQLite database. The script captures detailed block information, including transactions within each block, facilitating further analysis or integration into Ethereum-based applications.

## How It Works

1. **Fetch Block Data**: For each block number in the specified range, the script constructs a JSON payload to query the Ethereum JSON-RPC endpoint, fetching data for that block.

2. **Database Initialization**: On startup, the script checks for the existence of `blocks` and `transactions` tables within the specified SQLite database file, creating them if they do not exist.

3. **Data Insertion**: Each fetched block's data, along with its transactions, is inserted into the database, ensuring data persistence for further queries or analysis.

4. **Result Query**: After all specified blocks have been fetched and stored, the script executes a predefined query (`execute_result_query`) to retrieve or analyze the stored data, showcasing the script's ability to support custom data analysis needs.

## Prerequisites

- Python 3.x
- `requests` library for making HTTP requests.
- SQLite3 for database operations.

## Usage

To use the Ethereum Block Crawler, run the script from the command line, providing the necessary arguments:

```bash
python block-crawler.py <json_rpc_endpoint> <sqlite_file> <start_block-end_block>
```

### Arguments

- `<json_rpc_endpoint>`: The URL of the Ethereum JSON-RPC endpoint (e.g., `https://rpc.quicknode.pro/key`).
- `<sqlite_file>`: The path to the SQLite database file where the block and transaction data will be stored.
- `<start_block-end_block>`: The range of block numbers to fetch, specified as `start_block-end_block` (e.g., `9000000-9000100`).

## Example

```bash
python block-crawler.py https://yolo-dark-sanctuary.quiknode.pro/API_KEY/ db.sqlite3 18908800-18909050
```

This command will fetch blocks from 18,908,800 to 18,909,050 from the specified Ethereum JSON-RPC endpoint and store them in `db.sqlite3`.

## Features to add

