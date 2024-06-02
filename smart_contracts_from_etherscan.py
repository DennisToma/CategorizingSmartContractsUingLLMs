import requests
import json

# Function to fetch smart contract source code from Etherscan
def get_contract_source_code(api_key, contract_address):
    url = f'https://api.etherscan.io/api'
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': contract_address,
        'apikey': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if data['status'] == '1':
            return data['result'][0]['SourceCode']
        else:
            return f"Error: {data['result']} - {data['message']}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"

# Function to fetch byte-code of a smart contract from Etherscan
def get_contract_byte_code(api_key, contract_address):
    url = f'https://api.etherscan.io/api'
    params = {
        'module': 'proxy',
        'action': 'eth_getCode',
        'address': contract_address,
        'tag': 'latest',
        'apikey': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if 'result' in data:
            return data['result']
        else:
            return f"Error: {data} - {data.get('message', 'No message provided')}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"


# Main function to demonstrate fetching data
def main():
    # Replace with your Etherscan API key
    api_key = 'AN3212I5FMN92S1GTCXAU93RDZ9NC97JP2'
    # List of smart contract addresses you want to query
    contract_addresses = [
        '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',  # Uniswap V2 Router
        '0x514910771AF9Ca656af840dff83E8264EcF986CA',  # Chainlink Token (LINK)
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',  # USDC Stablecoin
        '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',  # Wrapped BTC (WBTC)
        '0x6B175474E89094C44Da98b954EedeAC495271d0F',  # DAI Stablecoin
    ]

    # Dictionary to store the data
    contracts_data = {}

    for contract_address in contract_addresses:
        print(f"Fetching data for contract address: {contract_address}")
        
        # Fetch the smart contract source code
        source_code = get_contract_source_code(api_key, contract_address)
        print("Source Code:")
        print(source_code)
        
        # Fetch the smart contract byte-code
        byte_code = get_contract_byte_code(api_key, contract_address)
        print("\nByte Code:")
        print(byte_code)
        print("\n" + "="*50 + "\n")
        
        # Store the data in the dictionary
        contracts_data[contract_address] = {
            'source_code': source_code,
            'byte_code': byte_code
        }

    # Save the data to a JSON file
    with open('contracts_data.json', 'w') as json_file:
        json.dump(contracts_data, json_file, indent=4)

if __name__ == '__main__':
    main()