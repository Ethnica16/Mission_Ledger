import hashlib
import datetime as date
import json

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp, content_hash, metadata):
        self.sender = sender  # e.g., "AI_Module"
        self.receiver = receiver  # e.g., "MissionControl"
        self.amount = amount  # text: the actual AI-generated content
        self.timestamp = timestamp
        self.content_hash = content_hash  # hash of AI-generated output
        self.metadata = metadata  # optional: mission_id, type, location, etc.

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": str(self.timestamp),
            "content_hash": self.content_hash,
            "metadata": self.metadata
        }

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = str(self.index) + str([tx.to_dict() for tx in self.transactions]) + str(self.timestamp) + self.previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2  

    def hash_data(self,data):
        """
        Returns the SHA-256 hash of the given data.
        Used to create a content hash for integrity.
        """
        data_string = json.dumps(data,sort_keys=True).encode()
        return hashlib.sha256(data_string).hexdigest()
    
    def create_genesis_block(self):
        genesis_tx = Transaction("Genesis", "Genesis", "Genesis Block", date.datetime.now(), "0"*64, {})
        return Block(0, [genesis_tx], date.datetime.now(), "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.pending_transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction")

    def mine_block(self, miner):
        if not self.pending_transactions:
            return False  # nothing to mine

        last_block = self.get_last_block()
        new_block = Block(len(self.chain), self.pending_transactions, date.datetime.now(), last_block.hash)
        self.chain.append(new_block)
        self.pending_transactions = []

        # Reward miner (optional logic)
        miner.reward()

        return new_block

class Miner:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def reward(self):
        self.balance += 1



