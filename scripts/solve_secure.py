from brownie import (
    network,
    accounts,
    config,
    interface,
    SecureSetup,
    SecureWallet,
    TokenModule
)
from scripts.helpful_scripts import (
    get_account,
    check_solution
)
from web3 import Web3


def main():
    deployer = get_account(index=0)
    attacker = get_account(index=1)

    # setup challenge
    setup = SecureSetup.deploy({"from": deployer, "value": Web3.toWei(50, 'ether')})
    weth = interface.IWETH9(setup.WETH())

    # solve challenge
    # did I hack success conditions again?
    # haha, this time the official solution is the same :D
    weth.deposit({"from": attacker, "value": Web3.toWei(50, 'ether')})
    weth.transfer(setup, Web3.toWei(50, 'ether'), {"from": attacker})

    # check the solution
    check_solution(setup)