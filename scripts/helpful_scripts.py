from brownie import (
    network,
    accounts,
    config,
    interface,
    Contract,
)
from brownie.network.state import Chain
from brownie import web3
from web3 import Web3

def get_account(index=None, id=None):
    if index is not None:
        return accounts[index]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

def get_web3():
    return Web3(web3.provider)

def check_solution(setup_contract):
    if setup_contract.isSolved():
        print("Challenge solved!")
    else:
        print("Challenge not solved...")

