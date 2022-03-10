from brownie import (
    network,
    chain,
    accounts,
    config,
    interface,
    HelloSetup,
    Hello
)
from scripts.helpful_scripts import (
    get_account,
    check_solution
)
from web3 import Web3


def main():
    deployer = get_account(index=0)
    player = get_account(index=1)

    # setup challenge
    setup_contract = HelloSetup.deploy({"from": deployer})
    hello_contract = Hello.at(setup_contract.hello())

    # solve challenge
    tx = hello_contract.solve({"from": player})
    tx.wait(1)

    # check the solution
    check_solution(setup_contract)
