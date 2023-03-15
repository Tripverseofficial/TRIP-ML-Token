from brownie import Trip, network
import pytest

@pytest.fixture
def trip():
    return Trip.deploy({'from': get_account()})

def test_initial_supply(trip):
    assert trip.totalSupply() == 1000000 * 10 ** 18
