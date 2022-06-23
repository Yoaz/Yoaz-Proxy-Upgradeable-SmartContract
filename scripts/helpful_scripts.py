from brownie import network, accounts, config
import eth_utils

LOCAL_BLOCKCHAIN_DEVELOPMET = {"development", "mainnet-fork", "ganache-local"}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.add[id]
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMET:
        return accounts.add(config["wallets"]["from_key"])
    return accounts[0]


# initalizer = sore, 1
def encode_function_data(initializer=None, *args):
    """
    Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if (
        len(args) == 0 or not initializer
    ):  # if we don't have any arguments in the initializer or not using an intializer
        return eth_utils.to_bytes(
            hexstr="0x"
        )  # then simply return empty hex string and then the smart contract will understand
    return initializer.encode_input(
        *args
    )  # otherwise encode the initializer with the args


def upgrade_transaction(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    """
    This function is a generic upgrade contract call
    it will act according to existent of initializer or not
    as well as if proxy_admin or not
    """
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_initializer_function = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_initializer_function,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_initializer_function = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address, encode_function_data, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from": account})
    return transaction
