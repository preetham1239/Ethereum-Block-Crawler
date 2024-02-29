import json
import sqlite3
import sys
import requests
from models.block import Block
from query import execute_result_query


# Function to fetch block data from the Ethereum JSON-RPC endpoint
def fetch_block_data(json_rpc_endpoint, block_number):
    request_payload = json.dumps({
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {'Content-Type': 'application/json'}

    # Make a POST request to the specified JSON-RPC endpoint
    response = requests.post(json_rpc_endpoint, headers=headers, data=request_payload)

    # Return a block object if request is successful else, raise an exception.
    if response.ok:
        return Block.from_json(response.json()['result'])
    else:
        raise Exception(f"Error fetching block {block_number}: {response.status_code}")


# Function to initialize the SQLite database with required tables
def initialize_database(connection):
    cursor = connection.cursor()
    # Create the 'blocks' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            hash TEXT PRIMARY KEY,
            number INTEGER,
            timestamp DATETIME
        )
    ''')
    # Create the 'transactions' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            txn_hash TEXT PRIMARY KEY,
            block_hash TEXT,
            block_number INTEGER,
            from_address TEXT,
            to_address TEXT,
            value REAL,
            FOREIGN KEY (block_hash) REFERENCES blocks(hash)
        )
    ''')
    connection.commit()


# Function to insert a block and its transactions into the database
def insert_block_and_transactions(connection, block):

    # Prepare the data for block and txn table
    block_data = (block.hash, block.number, block.timestamp)
    transactions_data = [
        (tx.txn_hash, tx.block_hash, tx.block_number, tx.from_address, tx.to_address, tx.value)
        for tx in block.transactions
    ]

    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO blocks (hash, number, timestamp) VALUES (?, ?, ?)
    ''', block_data)

    if transactions_data:
        cursor.executemany('''
            INSERT OR IGNORE INTO transactions 
            (txn_hash, block_hash, block_number, from_address, to_address, value) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', transactions_data)

    connection.commit()


# Main function to orchestrate the fetching and storing of block data
def main(json_rpc_endpoint, db_file_path, start_block, end_block):
    connection = sqlite3.connect(db_file_path)
    initialize_database(connection)

    # Iterate over the specified range of block numbers, fetch their data, and store in the database
    for block_num in range(start_block, end_block + 1):
        block = fetch_block_data(json_rpc_endpoint, block_num)
        insert_block_and_transactions(connection, block)
        print(f"Inserted transactions for block {block_num}")

    connection.close()

    # Execute a query to get the result
    execute_result_query(db_file_path)


if __name__ == "__main__":
    # Validate and parse command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python block-crawler.py <json_rpc_endpoint> <sqlite_file> <block_range>")
        sys.exit(1)

    # Extract command-line arguments
    rpc_endpoint = sys.argv[1]
    db_path = sys.argv[2]
    block_range = sys.argv[3].split('-')

    if len(block_range) != 2:
        print("Block range should be in the format 'start-end'")
        sys.exit(1)

    start_block = int(block_range[0])
    end_block = int(block_range[1])

    # Run the main function with the parsed arguments
    main(rpc_endpoint, db_path, start_block, end_block)
