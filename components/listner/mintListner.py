import requests


response = requests.get(
    "https://api.bscscan.com/api?module=logs&action=getLogs&fromBlock='latest'&toBlock='latest'&address=0x15e5F6a3Bf39D936b07cCE64637E760609c0c0a6&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&apikey=61F4XMH9YPHZNQJ914C6N7Q7ZEI5FYDY2H"
)

response = response.json()
data = response.get('result')
print(len(data))
