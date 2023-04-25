import requests
from config import API_KEY


def getInitialTransactionCount(contractAddress:str):
    '''
    This function returns the initial transaction count
    Args:
        contractAddress (str): The contract address
    
    Returns:
        int: The initial transaction count
    '''
    
    # Parameters for the API call
    start_block = 0
    end_block = 999999999
    
    # Make an API call to get the latest minted token
    response = requests.get(f'https://api-testnet.bscscan.com/api?module=account&action=txlist&address={contractAddress}&startblock={start_block}&endblock={end_block}&sort=asc&apikey=' + API_KEY)

    # Convert the response to JSON
    response = response.json()

    data_length = len(response['result'])

    return data_length