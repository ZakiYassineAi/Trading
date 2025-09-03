# safe_adapter.py
from typing import Dict, Any
import json
import uuid

class SafeAdapter:
    """
    Prepares a transaction payload for Gnosis Safe multisig execution.
    """

    def __init__(self, safe_address: str):
        self.safe_address = safe_address

    def build_tx(self, to: str, value: int, data: str, operation: int = 0) -> Dict[str, Any]:
        """
        Build a Gnosis Safe transaction proposal.
        :param to: Target contract address
        :param value: ETH value in wei
        :param data: Encoded contract call (hex string)
        :param operation: 0 = CALL, 1 = DELEGATECALL
        """
        tx = {
            "safeTxHash": str(uuid.uuid4()),  # mock hash for demo
            "safe": self.safe_address,
            "to": to,
            "value": value,
            "data": data,
            "operation": operation,
            "nonce": 0,
        }
        return tx

    def export_json(self, tx: Dict[str, Any]) -> str:
        """Return the tx as a JSON string for API submission"""
        return json.dumps(tx, indent=2)
