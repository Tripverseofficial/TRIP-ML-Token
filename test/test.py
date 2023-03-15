import brownie
from brownie import Trip, accounts

def test_trip_contract():
    # Deploy the contract
    trip = Trip.deploy("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", {'from': accounts[0]})

    # Check that the contract deployed successfully
    assert trip is not None

    # Check the initial state of the contract
    assert trip.basePrice() == 0.01 * 10 ** 18
    assert trip.lastPrice() == 0.01 * 10 ** 18
    assert trip.nextRebaseTime() == trip.block_timestamp() + 1 * 24 * 60 * 60
    assert trip.decimals() == 18
    assert trip.maxSupply() == 100000000 * 10 ** 18

    # Test the getPrice() function
    assert trip.getPrice() == trip.basePrice() * trip.lastPrice() // (1 * 10 ** 18)

    # Test the updateBasePrice() function
    trip.updateBasePrice({'from': accounts[0]})
    assert trip.basePrice() != 0.01 * 10 ** 18

    # Test the calculateRebaseInterval() function
    rebase_interval = trip.calculateRebaseInterval()
    assert rebase_interval == 24 * 60 * 60 or \
           rebase_interval == 12 * 60 * 60 or \
           rebase_interval == 6 * 60 * 60 or \
           rebase_interval == 1 * 60 * 60

    # Test the rebase() function
    with brownie.reverts("Max supply reached"):
        trip.rebase({'from': accounts[0]})
    assert trip.totalSupply() == 100000000 * 10 ** 18
    assert trip.nextRebaseTime() == trip.block_timestamp() + 1 * 24 * 60 * 60
