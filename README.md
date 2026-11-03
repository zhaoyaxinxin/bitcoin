# bitcoin

区块链基础及应用 · 课程实验代码仓库。

## Exercise 4 · 跨链原子交换（Cross-chain Atomic Swap）

在 BTC Testnet3 与 BCY Testnet（BlockCypher 测试网）两条链之间，实现 Alice 与 Bob 的
无信任币币交换：围绕一个只有 Alice 知道的秘密 `x`，链上只公开 `H(x)`。一旦 `x` 因赎回而
上链，双方都能取走对方锁定的币；若 `x` 永不公开，双方在锁定期后各自退款。

> **当前仓库为实验初始模板。** `swap_scripts.py` 的三个脚本函数、`keys.py` 的密钥、
> `swap.py` 的参数均待填写。实验说明 `Exercise4.pdf` 未纳入版本库。

### 目录

```
Exercise4/
├── swap.py              # 主入口：参数配置 + atomic_swap() 流程编排
├── swap_scripts.py      # 待实现：coinExchangeScript / Sig1 / Sig2
├── alice.py             # Alice 侧交易构造、签名、广播
├── bob.py               # Bob 侧交易构造、签名、广播
├── keys.py              # 待填写：4 个测试网密钥及派生地址
├── keygen.py            # BTC 测试网密钥生成
├── p2pkh.py             # P2PKH 脚本与单笔转账工具
├── split_test_coins.py  # UTXO 拆分工具
├── utils.py             # 交易构造/签名/校验/广播的公共函数
├── design_doc.txt       # 设计文档（对应练习 D 的 a/b/c/d 四问）
└── requirements.txt
```

### 待完成

1. **`keys.py`** —— 填入 Alice / Bob 在 BTC testnet3 与 BCY testnet 上的私钥。
   BTC 密钥用 `keygen.py` 生成，BCY 密钥可用 32 字节随机数。
2. **`swap.py`** —— 填写待花费的 UTXO、金额、两条链的当前区块高度、锁定期，
   注意 `alice_locktime` 必须大于 `bob_locktime`。
3. **`swap_scripts.py`** —— 本实验的核心：
   - `coinExchangeScript` —— 生成同时具备「哈希锁」与「双签退款」两条花费路径的 ScriptPubKey
   - `coinExchangeScriptSig1` —— 知道秘密 `x` 的接收方赎回时的 ScriptSig
   - `coinExchangeScriptSig2` —— 发送方与接收方共同签名退款时的 ScriptSig

### 运行

```bash
pip install -r requirements.txt
cd Exercise4
python swap.py
```

`swap.py` 中 `broadcast_transactions = False` 时为本地验证模式，不发起任何网络请求，
脚本会逐个调用 `VerifyScript` 校验 ScriptSig + ScriptPubKey。`alice_redeems` 分别取
`True`（赎回路径）与 `False`（退款路径）各运行一次。

### 参考

- [Atomic cross-chain trading](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading)
- [Bitcoin Script 操作码](https://en.bitcoin.it/wiki/Script)

### 环境

Python 3.12.9 · python-bitcoinlib 0.12.2 · requests
