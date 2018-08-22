import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

'''一个区块包含属性：索引(index), Unix时间戳(timestamp), 
交易列表(transactions), 工作量证明, 前一个区块的Hash值.
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
'''
#创建Blockchain类
class Blockchain(object):
	def __init__(self):
		self.chain= []					#储存区块链
		self.current_transactions = []	#储存交易

		#Create the genesis block 构造创世块
		self.new_block(previous_hash=1,proof=100)

	def new_block(self,proof,previous_hash=None):
		# creates a new Block and adds it to the chain
		# 创建一个新块并把它加到链上
		"""
		生成新块
		:param proof:<int>The proof given by the Proof of Work algorithm
		:param previous_hash: (Optional)<str>Hash of previous Block
		:return: <dict>New Block
		"""
		block = {
			'index': len(self.chain)+1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof':proof,
			'previous_hash':previous_hash or self.hash(self.chain[-1])
		}

		#Reset the current list of transactions
		self.current_transactions = []

		self.chain.append(block)
		return block
	def new_transaction(self):
		#Adds a new transaction to the list of transaction
		"""
		生成新的交易信息,并将信息加入到下一个待挖的区块中
		:param sender:<str>Address of the Sender
		:param recipient:<str>Address of the Recipient
		:param amount:<int>Amount
		:return:<int>The index of the Block that will hold this transaction
		"""
		self.current_transactions.append(
		{
			'sender':sender,
			'recipient':recipient,
			'amount':amount
		}
		)
		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		"""
		生成块的SHA-256 hash值
		:param block: <dict>Block
		:return: <str>
		"""
		# We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
		block_string == json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		#Returns the last Block in the chain
		pass

	def proof_of_work(self,last_proof):
		"""
		简单的工作量证明：
		查找一个p'使得hash(pp')以4个0开头
		p是上一个块的证明,p'是当前的证明
		:param last_proof: <int>
		:return: <int>
		"""
		proof = 0
		while self.valid_proof(last_proof,proof) is False:
			proof += 1

		return proof

	@staticmethod
	def valid_proof(last_proof,proof):
		"""
		验证证明：是否hash(last_proof,proof)以4个0开头
		:param last_proof: <int>Previous Proof
		:param proof: <int>Current Proof
		:return: <bool> True if correct, False if not.
		"""
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"