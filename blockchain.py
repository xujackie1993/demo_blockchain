#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import hashlib
import json
from uuid import uuid4
"""
区块的结构： 索引(index)， Unix时间戳(timestamp), 交易列表(transactions), 工作量证明(proof)，
以及前一个区块的hash值(previous_hash)
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
"""

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self, proof, previous_hash=None):
        '''
        生成新块
        :param proof:<int> The proof given by the Proof of Work algorithm
        :param previous_hash:(Optional) <str> Hash of previous Block
        :return: <dict> New Block
        '''
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        #Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        生成新交易信息,信息加入到下一个待挖的区块
        :param sender: <str>  Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block["index"] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        '''
        生成块的SHA-256 hash的值
        :param block: <dict> Block
        :return: <str>
        '''
        #We mush make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self, last_proof):
        '''
        简单的工作量证明：
        查找一个数p与前一个区块的proof拼接成的字符串的Hash值以4个零开头
        :param last_proof: <int>
        :return: <int>
        '''
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        '''
        splicing = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(splicing).hexdigest()
        return guess_hash[:4] == "0000"
