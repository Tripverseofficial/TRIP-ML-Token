from brownie import Trip, network, config

def deploy_trip():
    account = get_account()
    trip = Trip.deploy({'from': account})
    trip.initialize_model({'from': account})

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
