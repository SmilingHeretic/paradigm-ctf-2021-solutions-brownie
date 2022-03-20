from brownie import (
    accounts,
    LockboxSetup,
    LockboxExploit,
    Entrypoint
)
from scripts.helpful_scripts import (
    get_account,
    check_solution,
)
from web3 import Web3
from ecdsa import ecdsa, SECP256k1, SigningKey
import sha3
import binascii

def main():
    deployer = get_account(index=0)
    attacker = get_account(index=1)

    # setup challenge
    setup = LockboxSetup.deploy({"from": deployer})
    entrypoint = Entrypoint.at(setup.entrypoint())

    # solve challenge
    # in comments on etherscan for this address you can find that the private key of this mysterious address is 1.
    who_are_you = accounts.add(f"{'0'*63}1")
    print("Confirm 'who are you' account address:", who_are_you)
    print()

    exploit = LockboxExploit.deploy(entrypoint, {"from": attacker})
    r, s = find_signature(exploit, start_k=15434)
    tx = exploit.exploit(r, s, {"from": attacker})
    tx.wait(1)

    # I used lots of logs for debugging. There's contracts/lockbox/LockboxDebug.sol file where I left the logs.
    for key, value in tx.events.items():
        print(key)
        print(value)
        print()

    # check the solution
    check_solution(setup)

def find_signature(exploit, start_k=1):
    # private key 1 for "who are you" account to pass stage 1
    private_key = 31 * b'\00' + b'\01'
    # hashes used in lockbox contracts
    stage1_hash = hash_message('stage1')
    choose_hash = hash_message('choose')

    signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
    k = find_k(signing_key, stage1_hash, choose_hash, exploit, start_k)
    sig = signing_key.privkey.sign(stage1_hash, k)
    r = f"0x{sig.r:032x}"
    s = f"0x{sig.s:032x}"

    print()
    print("Found correct signature!")
    print(f"k={k}")
    print(f"r={r}")
    print(f"s={s}")
    print()
    return r, s

def find_k(signing_key, stage1_hash, choose_hash, exploit, start_k):
    # we need b argument in stage 2 to be at least this large to achieve overflow
    min_b = 2 ** 16 - 28

    k = start_k
    while True:
        sig = signing_key.privkey.sign(stage1_hash, k)

        # to get the overflow in stage 2 and pass "something doesn't add up"
        condition_1 = get_stage_2_b(sig) >= min_b
        # to pass "out of order" in stage 3. r, s (stage 1) are the same as keys[0], keys[1] (stage 3)
        condition_2 = sig.r < sig.s
        # In stage 4, we see that one element of keys has to be equal to the hash of "choose"
        # it has to be keys[2] or keys[3] (stage 3) so it has to be larger than keys[1] == sig.s to pass "out of order"
        # It cannot be lock[0] because we don't have control over last digit of choice (stage 4) because of calldata length limit in stage 5
        # and therefore (choice mod 6) mod 2 == 0, so choice mod 6 != 5
        condition_3 = sig.s < choose_hash
        # In stage 3 to pass "this is a bit odd" we need sig.s == keys[1] to be of the same parity as lock[1].
        # lock[1] has to be even because we don't have the control over its last digit because of calldata length constraints in stage 5
        condition_4 = sig.s % 2 == 0
        # Finally, v (stage 1) has to be 28, so idx mod 4 == 0 (stage 3). Otherwise, we'd have to set lock[n > 0] to some (non-zero) keys[n].
        # We don't have full control over these lock elements, so idx mod 4 has to be equal zero. v (stage 1) is equal to last byte of idx (stage 3)
        # Let's just test if our signature works with v=28 (as opposed to v=27).
        condition_5 = False
        # For speed, check only if all other conditions satisfied
        if condition_1 and condition_2 and condition_3 and condition_4:
            print(f'Found k={k} meeting first 4 conditions. Checking if it works with v=28...')
            condition_5 = exploit.testSignature(sig.r, sig.s)

        if k % 1000 == 0:
            print(f"checking k={k}")

        if condition_1 and condition_2 and condition_3 and condition_3 and condition_4 and condition_5:
            return k
        k += 1

def get_stage_2_b(sig):
    # b in stage 2 is the same as last two bytes of r from stage 1
    # I found it out empirically by printing logs but you can also calculate this 
    r = f"0x{sig.r:032x}"
    return int(r[-4:], base=16)

def hash_message(msg: str) -> int:
    """
    copied from babycrypto challenge

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