# bitcoin

区块链基础及应用 · 课程实验代码仓库。

## Exercise 4 · 跨链原子交换（Cross-chain Atomic Swap）

在 BTC Testnet3 与 BCY Testnet（BlockCypher 测试网）两条链之间，实现 Alice 与 Bob 的
无信任币币交换：围绕一个只有 Alice 知道的秘密 `x`，链上只公开 `H(x)`。一旦 `x` 因赎回而
上链，双方都能取走对方锁定的币；若 `x` 永不公开，双方在锁定期后各自退款。

> **本实验已完成。** 已实现 `swap_scripts.py` 的三个脚本函数，并在 `keys.py` 与
> `swap.py` 中填入双方的真实 UTXO 与参数。两条分支（`alice_redeems` 取 `True` /
> `False`）均运行通过，输出见 `run_redeem.txt` 与 `run_refund.txt`，
> 设计与原理说明见 `design_doc.txt`。

| 参与方 | 姓名 | 学号 | 角色 |
|---|---|---|---|
| Alice | 赵亚鑫 | 2413715 | BTC 侧参数、BCY 密钥、`swap_scripts.py` 实现 |
| Bob | 张煜坤 | 2413654 | BCY 侧参数与密钥 |

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
├── design_doc.txt       # 设计文档（对应练习 D 的 a/b/c/d 四问）
├── run_redeem.txt       # alice_redeems = True 的运行输出
├── run_refund.txt       # alice_redeems = False 的运行输出
└── requirements.txt
```

### 锁定脚本

`coinExchangeScript` 生成的 ScriptPubKey 同时具备「哈希锁」与「双签退款」两条花费路径：

```
OP_IF
    OP_HASH160 <H(x)> OP_EQUALVERIFY <pk_recipient> OP_CHECKSIG
OP_ELSE
    <pk_sender> OP_CHECKSIGVERIFY <pk_recipient> OP_CHECKSIG
OP_ENDIF
```

| 路径 | ScriptSig | 触发条件 |
|---|---|---|
| 哈希锁 | `[sig_recipient, x, OP_TRUE]` | 接收方知道 `x` 且能签名 |
| 双签退款 | `[sig_recipient, sig_sender, OP_FALSE]` | 发送方与接收方都签名 |

时间锁由退款交易的 `nLockTime` 承担——`coinExchangeScript` 的签名中没有 locktime
参数，无法在脚本里使用 `OP_CHECKLOCKTIMEVERIFY`。

### 运行

```bash
pip install -r requirements.txt
cd Exercise4
python swap.py
```

`swap.py` 中 `broadcast_transactions = False` 时为本地验证模式，不发起任何网络请求，
脚本会逐个调用 `VerifyScript` 校验 ScriptSig + ScriptPubKey。`alice_redeems` 分别取
`True`（赎回路径）与 `False`（退款路径）各运行一次。

本次提交按实验要求采用本地验证模式，未向区块链广播交易，因此链上查不到对应的交换交易。

### 参考

- [Atomic cross-chain trading](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading)
- [Bitcoin Script 操作码](https://en.bitcoin.it/wiki/Script)

### 环境

Python 3.12.9 · python-bitcoinlib 0.12.2 · requests
