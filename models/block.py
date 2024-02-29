from datetime import datetime
from models.transaction import Transaction


class Block:
    def __init__(self, hash, number, timestamp, transactions):
        self.hash = hash
        self.number = number
        self.timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self.transactions = [Transaction(
            txn_hash=tx['hash'],
            block_hash=tx['blockHash'],
            block_number=int(tx['blockNumber'], 16),
            from_address=tx['from'],
            to_address=tx['to'],
            value=int(tx['value'], 16) / 1e18
        ) for tx in transactions]

    @staticmethod
    def from_json(data):
        return Block(
            hash=data['hash'],
            number=int(data['number'], 16),
            timestamp=int(data['timestamp'], 16),
            transactions=data['transactions']
        )
