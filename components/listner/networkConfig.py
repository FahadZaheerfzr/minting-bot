class NetworkConfig:
    def __init__(self, network: str):
        self.network = network
        self.api_url = None
        self.rpc_url = None
        self.chain_id = None
        self.set_network_config()

    def set_network_config(self):
        if self.network == "eth_mainnet":
            self.api_url = "https://api.etherscan.io/api"
            self.rpc_url = "https://rpc.ankr.com/eth"
            self.chain_id = 1
        elif self.network == "bsc_mainnet":
            self.api_url = "https://api.bscscan.com/api"
            self.rpc_url = "https://rpc.ankr.com/bsc"
            self.chain_id = 56
        elif self.network == "bsc_testnet":
            self.api_url = "https://api-testnet.bscscan.com/api"
            self.rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
            self.chain_id = 97
        elif self.network == "roburna_mainnet":
            self.api_url = "https://rbascan.com/api/v2"
            self.rpc_url = "https://dataseed.roburna.com"
            self.chain_id = 158

        else:
            raise ValueError("Invalid network selected.")

    def get_api_key(self) -> str:
        if self.network == "eth_mainnet":
            return "TD5DWIURXH2GJ663FSNV9VENI14DK9RUAZ"
        elif self.network == "bsc_mainnet":
            return "61F4XMH9YPHZNQJ914C6N7Q7ZEI5FYDY2H"
        elif self.network == "bsc_testnet":
            return "978IQ2RMN1VHGMG3BMJRI5UYSAX8UN5Z7U"
        else:
            raise ValueError("Invalid network selected.")