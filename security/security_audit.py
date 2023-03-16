# Script to perform security audit on smart contract

from brownie import *
import os

# Load the smart contract
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
contract_file = os.path.join(project_folder, "contracts", "trip.sol")
contract = Contract.from_abi("MyContract", address="0x0000000000000000000000000000000000000000", abi=compile_source(open(contract_file, "r").read()).encode_abi())

# Print all functions in the smart contract
print("Functions in Smart Contract:")
for func in contract:
    print("- " + func)

# Print all events in the smart contract
print("Events in Smart Contract:")
for event in contract.events:
    print("- " + event)

# Print all variables in the smart contract
print("Variables in Smart Contract:")
for var in contract.vars:
    print("- " + var)

# Check for reentrancy vulnerabilities
print("Checking for reentrancy vulnerabilities...")
assert not contract.reentrancy()

# Check for integer overflow/underflow vulnerabilities
print("Checking for integer overflow/underflow vulnerabilities...")
assert not contract.overflow()

# Check for denial of service vulnerabilities
print("Checking for denial of service vulnerabilities...")
assert not contract.dos()
