from bitcoin.core.script import *


def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        OP_IF,
            OP_HASH160, hash_of_secret, OP_EQUALVERIFY,
            public_key_recipient, OP_CHECKSIG,
        OP_ELSE,
            public_key_sender, OP_CHECKSIGVERIFY,
            public_key_recipient, OP_CHECKSIG,
        OP_ENDIF,
    ]


def coinExchangeScriptSig1(sig_recipient, secret):
    return [sig_recipient, secret, OP_TRUE]


def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [sig_recipient, sig_sender, OP_FALSE]
