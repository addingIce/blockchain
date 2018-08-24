# Create a simple blockchain with python
## 一、环境准备
*python3.6+*
## 二、创建Blockchain
### 1. Blockchain类
*在构造函数中创建了两个列表，一个用于储存区块链，一个用于储存交易。*
```
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
```
### 2. 块结构
*每个区块包含属性：索引（index），Unix时间戳（timestamp），交易列表（transactions），工作量证明（稍后解释）以及前一个区块的Hash值。*
```
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
```
## 三、Blockchain作为API接口
*我们将使用Python Flask框架，这是一个轻量Web应用框架，它方便将网络请求映射到 Python函数*

我们将创建三个接口：
1.**/transactions/new** 创建一个交易并添加到区块
发送到节点的交易数据结构如下：
```
{
 "sender": "my address",
 "recipient": "someone else's address",
 "amount": 5
}
```
2.**/mine** 告诉服务器去挖掘新的区块
挖矿正是神奇所在，它很简单，做了一下三件事：
```
1. 计算工作量证明PoW
2. 通过新增一个交易授予矿工（自己）一个币
3. 构造新区块并将其添加到链中
```
3.**/chain** 返回整个区块链
## 四、一致性（共识）
*我们已经有了一个基本的区块链可以接受交易和挖矿。但是区块链系统应该是分布式的。既然是分布式的，那么我们究竟拿什么保证所有节点有同样的链呢？这就是一致性问题，我们要想在网络上有多个节点，就必须实现一个一致性的算法。*
### 1. 注册节点
*在实现一致性算法之前，我们需要找到一种方式让一个节点知道它相邻的节点。每个节点都需要保存一份包含网络中其它节点的记录。因此让我们新增几个接口：*

1.**/nodes/register** 接收URL形式的新节点列表
```
{
	"nodes": ["http://127.0.0.1:5000", "http://127.0.0.1:5001"]
}
```
2.**/nodes/resolve** 执行一致性算法，解决任何冲突，确保节点拥有正确的链

### 2.实现共识算法
*前面提到，冲突是指不同的节点拥有不同的链，为了解决这个问题，规定最长的、有效的链才是最终的链，换句话说，网络中有效最长链才是实际的链。*

## 五、运行区块链
*你可以使用Postman 去和API进行交互*





