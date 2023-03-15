from brownie import Trip, network, config, accounts

def deploy_contract(contract_type):
    """
    Deploys a contract of the specified type.
    """
    account = get_account()
    contract = contract_type.deploy({'from': account})
    return contract

def initialize_model(contract):
    """
    Initializes the model of the specified contract.
    """
    account = get_account()
    contract.initialize_model({'from': account})

def get_account():
    """
    Returns the default account to use for deployments.
    """
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

if __name__ == "__main__":
    # Deploy the Trip contract
    trip_contract = deploy_contract(Trip)

    # Initialize the Trip contract model
    initialize_model(trip_contract)
