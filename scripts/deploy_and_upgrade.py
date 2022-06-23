from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from scripts.helpful_scripts import (
    get_account,
    encode_function_data,
    upgrade_transaction,
)


def deploy_box():
    account = get_account()
    print("Deploying contract at '{}' network".format(network.show_active()))
    box = Box.deploy({"from": account}, publish_source=True)
    print("Contract deployed at address: {}".format(box.address))

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    # initializer = box.store, 1 --> in case we have an initializer (we chose no initializer in this case)
    box_encoded_initializer_function = (
        encode_function_data()
    )  # Passing nothing, has we don't have an initializer

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )
    print(f"Proxy contract deplyoed at: {proxy.address}")
    # Paste abi of another contract to a contract will paste all functionallity to that contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # For testing
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    # Upgrade
    box_v2 = BoxV2.deploy({"from": account})
    print("V2 contract deploy at: {}".format(box_v2.address))
    upgraded_transaction = upgrade_transaction(
        account, proxy, box_v2.address, proxy_admin
    )
    upgraded_transaction.wait(1)
    print(f"Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())


def main():
    deploy_box()
