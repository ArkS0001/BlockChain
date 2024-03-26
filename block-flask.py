import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create the first block (genesis block) of the blockchain
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        # Return the latest block in the blockchain
        return self.chain[-1]

    def add_block(self, new_block):
        # Add a new block to the blockchain
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Instantiate the Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    # Mining a new block
    previous_block = blockchain.get_latest_block()
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    data = "Block " + str(index)
    previous_hash = previous_block.hash
    new_block = Block(index, timestamp, data, previous_hash)
    blockchain.add_block(new_block)
    response = {
        'message': 'Block mined successfully!',
        'index': new_block.index,
        'timestamp': str(new_block.timestamp),
        'data': new_block.data,
        'previous_hash': new_block.previous_hash,
        'hash': new_block.hash
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    # Get the full blockchain
    response = {
        'chain': json.dumps([vars(block) for block in blockchain.chain]),
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# Running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
