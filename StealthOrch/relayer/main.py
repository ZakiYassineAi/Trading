from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from eth_account.messages import encode_typed_data # Corrected import
from eth_account import Account

# --- Pydantic Models ---
class ExecuteRequest(BaseModel):
    permit_payload: Dict[str, Any]
    signature: str

class ExecuteResponse(BaseModel):
    status: str
    tx_hash: str

# --- FastAPI App ---
app = FastAPI(
    title="StealthOrch Relayer",
    description="A service to execute signed EIP-712 permits.",
    version="0.1.0",
)

@app.post("/execute", response_model=ExecuteResponse)
async def execute_permit(request: ExecuteRequest):
    """
    Accepts a signed EIP-712 permit, validates it, and broadcasts the transaction.
    (Currently mocked)
    """
    print("--- RELAYER: Received /execute request ---")

    permit = request.permit_payload
    signature = request.signature

    # --- 1. Mock Signature Validation ---
    print(f"--> Mock validating signature: {signature[:10]}...")
    try:
        # In a real implementation, you'd use encode_structured_data and recover_message
        # For now, we just check if the signature looks like a hex string
        assert signature.startswith("0x") and len(signature) > 10
        print("    ✅ Mock signature format is valid.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    # --- 2. Mock Expiry and Nonce Check ---
    print("--> Mock checking expiry and nonce...")
    # In a real implementation, you would check `permit['message']['deadline']`
    # and look up the nonce in a database.
    print("    ✅ Mock expiry and nonce are valid.")

    # --- 3. Mock Transaction Broadcast ---
    print("--> Mock broadcasting transaction...")
    # In a real implementation, you would use your funded relayer key to send the tx.
    mock_tx_hash = f"0x_relayed_{hash(signature)}"
    print(f"    ✅ Mock transaction broadcasted with hash: {mock_tx_hash}")

    return {
        "status": "SUBMITTED_BY_RELAYER",
        "tx_hash": mock_tx_hash
    }

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
