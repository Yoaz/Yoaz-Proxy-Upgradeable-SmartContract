from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
from scripts.helpful_scripts import encode_function_data, upgrade_transaction
from scripts.helpful_scripts import get_account, encode_function_data
import pytest


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_box_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_box_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    # Upgrade
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_v2.abi)
    # Trying to call method from upgraded contract that isn't available on current contract
    # Expecting 'VirtualMachingError' to raise, therefore test will pass if error will be raised
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    tx = upgrade_transaction(account, proxy, box_v2.address, proxy_admin)
    tx.wait(1)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
