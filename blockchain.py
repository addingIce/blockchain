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

	def new_block(self):
		#creates a new Block and adds it to the chain
		#创建一个新块并把它加到链上
		pass

	def new_transaction(self):
		#Adds a new transaction to the list of transaction
		"""
		生成新的交易信息,并将信息加入到下一个待挖的区块中
		:param sender:<str>Address of the Sender
		
		"""

	@staticmethod
	def hash(block):
		#Hashs a Block
		pass

	@property
	def last_block(self):
		#Returns the last Block in the chain
		pass