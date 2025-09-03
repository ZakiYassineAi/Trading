import os
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv(dotenv_path='StealthOrch/.env')

class Settings:
    # Database
    DB_PATH: str = os.getenv("DB_PATH", "sqlite:///./StealthOrch/default.db")

    # Whitelist
    WHITELIST_PATH: str = os.getenv("WHITELIST_PATH", "./StealthOrch/whitelist.example.json")

    # RPC Endpoints
    RPC_MAINNET: str = os.getenv("RPC_MAINNET")
    RPC_ARBITRUM: str = os.getenv("RPC_ARBITRUM")
    RPC_SEPOLIA: str = os.getenv("RPC_SEPOLIA")

    # Gnosis Safe
    DEFAULT_SAFE_ADDRESS: str = os.getenv("DEFAULT_SAFE_ADDRESS")

    # Relayer
    RELAYER_URL: str = os.getenv("RELAYER_URL")

    def get_rpc_url(self, chain: str) -> str:
        """Gets the RPC URL for a given chain."""
        rpc_var_name = f"RPC_{chain.upper()}"
        url = getattr(self, rpc_var_name, None)
        if not url:
            raise ValueError(f"RPC URL for chain '{chain}' not found in settings (expected {rpc_var_name})")
        return url

settings = Settings()
