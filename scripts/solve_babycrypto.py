from ecdsa import ecdsa, SigningKey, SECP256k1
import sha3
import binascii


def print_signature(message_1, message_2, r, s_1, s_2, test_hash):
    # hash messages
    m_1 = hash_message(message_1)
    m_2 = hash_message(message_2)
    
    # convert hex strings to  ints
    r = int(r, base=16)
    s_1 = int(s_1, base=16)
    s_2 = int(s_2, base=16)
    test_hash = int(test_hash, base=16)
    
    # recover private_key
    private_key = recover_private_key(m_1, m_2, r, s_1, s_2)
    
    # convert private key to bytes
    private_key = bytes.fromhex(hex(private_key)[2:])
    
    # sign the test message
    signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
    sig = signing_key.privkey.sign(test_hash, 1)
    
    # convert r and d to hex strings
    r = f"0x{sig.r:032x}"
    s = f"0x{sig.s:032x}"
    
    # print the solution
    print(f"r={r}")
    print(f"s={s}")

def recover_private_key(m_1, m_2, r, s_1, s_2):
    # here's described why it works: https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/
    order = ecdsa.generator_secp256k1.order()
    k = (pow((s_1 - s_2), -1, order) * (m_1 - m_2)) % order
    private_key = (pow(r, -1, order) * (k * s_1 - m_1)) % order
    print("session_secret:", k)
    print("private_key:", private_key)
    print()
    return private_key

def hash_message(msg: str) -> int:
    """
    hash the message using keccak256, truncate if necessary
    """
    k = sha3.keccak_256()
    k.update(msg.encode("utf8"))
    d = k.digest()
    n = int(binascii.hexlify(d), 16)
    olen = ecdsa.generator_secp256k1.order().bit_length() or 1
    dlen = len(d)
    n >>= max(0, dlen - olen)
    return n

def main():
    message_1 = input("message? ")
    r = input("r? ")
    s_1 = input("s? ")
    message_2 = input("message? ")
    s_2 = input("s? ")
    test_hash = input("test? ")
    print()
    print_signature(message_1, message_2, r, s_1, s_2, test_hash)