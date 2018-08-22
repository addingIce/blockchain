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
#-------------创建Blockchain类----------------
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

	def new_transaction(self, sender, recipient, amount):
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
		return self.chain[-1]

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

#-------创建节点,Flask服务器将扮演区块链网络中的一个节点------

#Instantiate our Node 实例化
app = Flask(__name__)

#Generate a globally unique address for this node
#为节点创建一个名字(地址)
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Blockchain
#实例Blockchain类
blockchain = Blockchain()

#创建/mine GET接口,挖掘新块
"""
1.计算工作量证明PoW
2.通过新增一个交易授予矿工(自己)一个币
3.构造新区块并将其添加到链中
"""
@app.route('/mine', methods = ['GETA'])
def mine():
	#We run the proof of work algorithm to get the next proof
	last_block = blockchain.last_block
	last_proof = last_block['proof']
	proof = blockchain.proof_of_work(last_proof)

	#给工作量证明的节点提供奖励.
	#发送者为"0"表明是新挖出的币
	blockchain.new_transaction(
		sender = "0",
		recipient = node_identifier,
		amount = 1
	)

	#Forge the new Block by adding it to the chain
	block = blockchain.new_block(proof)

	response = {
		'message': "New Block Forged",
		'index': block['index'],
		'transactions': block['transactions'],
		'proof': block['proof'],
		'previous_hash': block['previous_hash']
	}

	return jsonify(response), 200

#创建/transactions/new POST接口,创建一个交易并添加到新块
@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
	values = request.get_json()

	#Check that the required fields are in the POST'ed data
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'Missing values', 400

	#Create a new Transaction
	index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

	response = {'message': f'Transaction will be added to Block{index}'}
	return jsonify(response), 201

#创建/chain接口,返回整个区块链
@app.route('/chain', methods = ['GET'])
def full_chain():
	response = {
		'chain': blockchain.chain,
		'length': len(blockchain.chain)
	}
	return jsonify(response), 200

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port=5000)