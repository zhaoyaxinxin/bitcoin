from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import x

SelectParams('testnet')

alice_secret_key_BTC = CBitcoinSecret(
    'cRTUBePmkbaC7LKD1cJvqRkhhePcUBdJiXcUzzBCvGfErwqEuAz2')

bob_secret_key_BTC = CBitcoinSecret(
    'cTdgTL9SKkqndopkgw8s1DsPHg2SUZhkrKnvWzw3Cj8pP4hFLCAh')

alice_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('c97b412707d724a588a8efffeb2697f2950b3bd8a200e3d3db8fc75740d4e546'))

bob_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('7ccb74982095bba2b8b8014d6bceaf43eae9a360f4e446fa5893c5ee856a2835'))

alice_public_key_BTC = alice_secret_key_BTC.pub
alice_address_BTC = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BTC)

bob_public_key_BTC = bob_secret_key_BTC.pub
bob_address_BTC = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BTC)

alice_public_key_BCY = alice_secret_key_BCY.pub
alice_address_BCY = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BCY)

bob_public_key_BCY = bob_secret_key_BCY.pub
bob_address_BCY = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BCY)
