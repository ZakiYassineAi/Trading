from typing import Dict, Any
import os

from .models import Opportunity

async def build_and_simulate_tx(opportunity: Opportunity, rpc_url: str) -> Dict[str, Any]:
    """
    Builds an unsigned transaction for an opportunity.
    NOTE: The web3 connection and simulation are currently MOCKED due to sandbox
    network limitations. This function returns a hardcoded successful result.
    """
    print("--- MOCKED TX BUILDER: Simulating successful transaction build ---")
    try:
        # This part is mocked. In a real environment, it would connect to web3.
        # w3 = Web3(Web3.HTTPProvider(rpc_url))
        # if not w3.is_connected():
        #     raise ConnectionError(f"Failed to connect to RPC for chain {opportunity.chain} at {rpc_url}")

        # Mocked data instead of real web3 calls
        mock_chain_id = 11155111 # Sepolia chain ID
        mock_gas_estimate = 100000

        # Create a mock unsigned transaction payload.
        # Include the opportunity ID in the data to ensure the payload hash is unique for each test.
        mock_data = f"0x4e71d92d{opportunity.id:064x}"

        unsigned_tx = {
            "to": opportunity.contract_address,
            "data": mock_data,
            "value": 0,
            "gas": mock_gas_estimate,
            "chainId": mock_chain_id,
        }

        return {"success": True, "unsigned_tx": unsigned_tx}

    except Exception as e:
        print(f"Error in (mocked) build_and_simulate_tx: {e}")
        return {"success": False, "error": str(e)}
