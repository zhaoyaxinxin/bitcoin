# bitcoin

区块链基础及应用 · 课程实验代码仓库。

## Exercise 4 · 跨链原子交换（Cross-chain Atomic Swap）

在 BTC Testnet3 与 BCY Testnet（BlockCypher 测试网）两条链之间，实现 Alice 与 Bob 的
无信任币币交换：围绕一个只有 Alice 知道的秘密 `x`，链上只公开 `H(x)`。一旦 `x` 因赎回而
上链，双方都能取走对方锁定的币；若 `x` 永不公开，双方在锁定期后各自退款。

### 目录

```
Exercise4/
├── swap.py              # 主入口：参数配置 + atomic_swap() 流程编排
├── swap_scripts.py      # 核心：coinExchangeScript / Sig1 / Sig2
├── alice.py             # Alice 侧交易构造、签名、广播
├── bob.py               # Bob 侧交易构造、签名、广播
├── keys.py              # 4 个测试网密钥及派生地址
├── keygen.py            # BTC 测试网密钥生成
├── p2pkh.py             # P2PKH 脚本与单笔转账工具
├── split_test_coins.py  # UTXO 拆分工具
├── utils.py             # 交易构造/签名/校验/广播的公共函数
├── requirements.txt
├── design_doc.txt       # 设计文档（对应练习 D 的 a/b/c/d 四问）
├── run_redeem.txt       # alice_redeems = True 的运行输出
└── run_refund.txt       # alice_redeems = False 的运行输出
```

### 锁定脚本

`coinExchangeScript` 生成一个同时具备「哈希锁」与「双签退款」两种花费路径的 ScriptPubKey：

```
OP_IF
    OP_HASH160 <H(x)> OP_EQUALVERIFY <pk_recipient> OP_CHECKSIG
OP_ELSE
    <pk_sender> OP_CHECKSIGVERIFY <pk_recipient> OP_CHECKSIG
OP_ENDIF
```

两条解锁路径：

| 路径 | ScriptSig | 条件 |
|---|---|---|
| 哈希锁 | `[sig_recipient, x, OP_TRUE]` | 接收方知道 `x` 且能签名 |
| 双签退款 | `[sig_recipient, sig_sender, OP_FALSE]` | 发送方与接收方都签名 |

时间锁由退款交易的 `nLockTime` 承担（脚本签名中没有 locktime 参数，无法使用
`OP_CHECKLOCKTIMEVERIFY`）。

### 运行

```bash
pip install -r requirements.txt
cd Exercise4
python swap.py
```

按实验要求以本地验证模式运行（`broadcast_transactions = False`，不向区块链广播）：

- `alice_redeems = True` —— 走赎回路径，`x` 公开，双方各自换取对方币
- `alice_redeems = False` —— 走退款路径，锁定期后双方各取回本金

两种模式均已跑通，输出见 `run_redeem.txt` 与 `run_refund.txt`。

### 参数

| 项 | 值 |
|---|---|
| BTC Testnet3 链高度 | 4,997,970 |
| BCY Testnet 链高度 | 2,611,494 |
| `alice_locktime` / `bob_locktime` | 5 / 3（块，必须 alice > bob） |
| 金额 | 0.1 BTC / 0.01 BCY，`tx_fee = 0.001` |

> 说明：本次为本地验证模式，未做链上广播，因此 `swap.py` 中的 txid 是合法的 64 位十六进制
> 占位值，不对应真实 UTXO。若要实际上链，替换 txid、utxo_index、金额并置
> `broadcast_transactions = True` 即可，脚本与流程无需改动。

### 环境

Python 3.12.9 · python-bitcoinlib 0.12.2 · requests
