# eip712_builder.py
from typing import Dict, Any
import time

class EIP712Builder:
    """
    Builds an EIP-712 structured data payload for signing.
    """

    def __init__(self, chain_id: int, verifying_contract: str):
        self.chain_id = chain_id
        self.verifying_contract = verifying_contract

    def build_permit(self, owner: str, spender: str, value: int, nonce: int, deadline: int = None) -> Dict[str, Any]:
        if deadline is None:
            deadline = int(time.time()) + 3600  # 1h expiry by default

        domain = {
            "name": "Token",
            "version": "1",
            "chainId": self.chain_id,
            "verifyingContract": self.verifying_contract,
        }

        types = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Permit": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
            ],
        }

        message = {
            "owner": owner,
            "spender": spender,
            "value": value,
            "nonce": nonce,
            "deadline": deadline,
        }

        payload = {
            "types": types,
            "domain": domain,
            "primaryType": "Permit",
            "message": message,
        }

        return payload
