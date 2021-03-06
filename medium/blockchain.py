'''
Step-by-step Guide
https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
'''

import hashlib
import json
from time import time

class Blockchain():

    def __init__(self):
        self.chain = []
        self.transactions = []

        # Create genesis block.
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        '''
        Creates a new block in the blockchain.

        :param proof: <int> Proof given by our proof of work algorithm.
        :param previous_hash: <str> Hash of previous block.
        :return: <dict> New block
        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        Creates a new transaction for the next mined block.

        :param sender: <str> Address of the sender.
        :param recipient: <str> Address of the recipient.
        :param amount: <int> Amount.
        :return: <int> The index of the block for this transaction.
        '''
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.transactions.append(transaction)
        return self.last_block.get('index') + 1

    def proof_of_work(self, last_proof):
        '''
        Find a number that when multipled by the last_proof has 'n' leading 0s
        as a proof of work algorithm. This is a simple implemetation.
        '''
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, leading_zeros=4):
        '''
        Returns whether the two multipled numbers have 4 leading zeros.

        :return: <bool>
        '''
        guess_hash = hashlib.sha256(str(last_proof * proof).encode()).hexdigest()
        return guess_hash[:leading_zeros] == ('0' * leading_zeros)

    @staticmethod
    def hash(block):
        '''
        Creates a SHA-256 hash of a block.

        :param block: <dict>
        :return: <str>
        '''
        # Ensure that the json is ordered to get deterministic hash.
        block_json = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_json).hexdigest()

    @property
    def last_block(self):
        '''
        Returns the last block in the blockchain.
        '''
        return self.transactions[-1]
