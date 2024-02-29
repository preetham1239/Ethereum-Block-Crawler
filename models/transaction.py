class Transaction:
    def __init__(self, txn_hash, block_hash, block_number, from_address, to_address, value):
        self.txn_hash = txn_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
