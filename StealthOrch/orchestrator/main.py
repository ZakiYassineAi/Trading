import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from pydantic import BaseModel, Field
from typing import List, Optional, Any

from . import models
from .database import create_db_and_tables, get_db
from .config import settings

# Create all tables
# In a real production app, you would use Alembic for migrations.
create_db_and_tables()

app = FastAPI(
    title="StealthOrch",
    description="Execution Orchestrator for Airdrop Collector",
    version="0.1.0",
)

# Setup templates
templates = Jinja2Templates(directory="StealthOrch/orchestrator/templates")


@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Serves the main admin dashboard UI.
    """
    prepared_txs = db.query(models.PreparedTx).options(joinedload(models.PreparedTx.opportunity)).order_by(models.PreparedTx.created_at.desc()).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "prepared_txs": prepared_txs}
    )


# Pydantic Schemas for API validation

class OpportunityBase(BaseModel):
    project: str
    contract_address: str
    function_name: str
    args: Optional[dict] = {}
    chain: str
    evidence: Optional[str] = None
    priority: int = 0

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    detected_at: datetime.datetime
    status: str

    class Config:
        from_attributes = True


@app.post("/opportunities", response_model=Opportunity, status_code=201)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    """
    Accepts a new airdrop opportunity and stores it in the database.
    """
    db_opportunity = models.Opportunity(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

@app.get("/healthz")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.
    """
    try:
        # A simple query to check DB connection, using the text() construct for SQLAlchemy 2.0
        db.execute(text('SELECT 1'))
        db_status = "ok"
    except Exception as e:
        print(f"Health check DB error: {e}")
        db_status = "error"

    return {
        "status": "ok",
        "database_status": db_status,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/opportunities", response_model=List[Opportunity])
def get_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all opportunities.
    """
    opportunities = db.query(models.Opportunity).offset(skip).limit(limit).all()
    return opportunities

# More Pydantic Schemas
class PreparedTx(BaseModel):
    id: int
    opportunity_id: int
    mode: str
    status: str
    payload_hash: str
    payload: dict # Including payload for testing and UI purposes

    class Config:
        from_attributes = True

from . import tx_builder
from StealthOrch.adapters import safe_adapter, eip712_builder
import hashlib
import json
import aiohttp

@app.post("/prepare/{opportunity_id}", response_model=PreparedTx)
async def prepare_opportunity_tx(opportunity_id: int, mode: str = "raw", db: Session = Depends(get_db)):
    """
    Prepares a transaction payload for a given opportunity based on the selected mode.
    Modes: 'raw', 'safe', 'relayer'
    """
    db_opportunity = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not db_opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    if db_opportunity.status != 'new':
        raise HTTPException(status_code=400, detail=f"Opportunity already has status '{db_opportunity.status}'")

    payload = {}

    if mode == 'raw':
        # The 'raw' mode prepares a standard unsigned transaction, similar to the original implementation.
        # This payload could be used with a manual wallet import or a simple QR code flow.
        result = await tx_builder.build_and_simulate_tx(db_opportunity, settings.get_rpc_url(db_opportunity.chain))
        if not result.get("success"):
            # Error handling logic...
            raise HTTPException(status_code=400, detail={"error": "Raw tx preparation failed", "reason": result.get("error")})
        payload = result["unsigned_tx"]

    elif mode == 'safe':
        # The 'safe' mode prepares a Gnosis Safe transaction proposal.
        if not settings.DEFAULT_SAFE_ADDRESS:
            raise HTTPException(status_code=500, detail="DEFAULT_SAFE_ADDRESS is not configured.")

        adapter = safe_adapter.SafeAdapter(settings.DEFAULT_SAFE_ADDRESS)
        # We need the raw calldata from the tx_builder
        raw_tx_result = await tx_builder.build_and_simulate_tx(db_opportunity, settings.get_rpc_url(db_opportunity.chain))
        if not raw_tx_result.get("success"):
            raise HTTPException(status_code=400, detail={"error": "Safe tx preparation failed during simulation", "reason": raw_tx_result.get("error")})

        unsigned_tx = raw_tx_result["unsigned_tx"]
        payload = adapter.build_tx(
            to=unsigned_tx['to'],
            value=unsigned_tx.get('value', 0),
            data=unsigned_tx['data']
        )

    elif mode == 'relayer':
        # The 'relayer' mode prepares an EIP-712 permit message for signing.
        # This is a simplified example. A real implementation would need more details.
        chain_id = 1 # This should come from the opportunity or a lookup
        builder = eip712_builder.EIP712Builder(chain_id=chain_id, verifying_contract=db_opportunity.contract_address)
        payload = builder.build_permit(
            owner="0xYourAddressHere", # This should come from the user session
            spender="0xRelayerAddressHere", # The address of the relayer
            value=db_opportunity.args.get('amount', 0),
            nonce=0 # Nonce should be managed per user
        )

    else:
        raise HTTPException(status_code=400, detail=f"Invalid mode '{mode}'. Valid modes are 'raw', 'safe', 'relayer'.")

    # Create and save the prepared transaction
    payload_str = json.dumps(payload, sort_keys=True)
    payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

    db_prepared_tx = models.PreparedTx(
        opportunity_id=opportunity_id,
        mode=mode,
        payload=payload,
        payload_hash=payload_hash,
        status="PREPARED"
    )
    db.add(db_prepared_tx)

    db_opportunity.status = 'prepared'

    db.commit()
    db.refresh(db_prepared_tx)

    return db_prepared_tx

class SubmitSafeResponse(BaseModel):
    proposal_id: str
    status: str

@app.post("/submit_safe/{prepared_id}", response_model=SubmitSafeResponse)
async def submit_safe_proposal(prepared_id: int, db: Session = Depends(get_db)):
    """
    Submits a prepared 'safe' mode transaction to the Gnosis Safe service.
    (Currently mocked)
    """
    db_prepared_tx = db.query(models.PreparedTx).filter(models.PreparedTx.id == prepared_id).first()

    if not db_prepared_tx:
        raise HTTPException(status_code=404, detail="Prepared transaction not found")
    if db_prepared_tx.mode != 'safe':
        raise HTTPException(status_code=400, detail="This endpoint is only for 'safe' mode transactions.")
    if db_prepared_tx.status != 'PREPARED':
        raise HTTPException(status_code=400, detail=f"Transaction is not in 'PREPARED' state, but '{db_prepared_tx.status}'.")

    # In a real implementation, this would call the Gnosis Safe Transaction Service API
    print(f"--- MOCK: Submitting to Gnosis Safe API for prepared_id: {prepared_id} ---")
    mock_proposal_id = f"safe_proposal_{hashlib.sha256(str(db_prepared_tx.payload).encode()).hexdigest()[:10]}"

    db_prepared_tx.status = 'SUBMITTED_TO_SAFE'
    db.commit()

    return {"proposal_id": mock_proposal_id, "status": "SUBMITTED_TO_SAFE"}

class SubmitPermitRequest(BaseModel):
    signature: str

class SubmitPermitResponse(BaseModel):
    relayer_tx_hash: str
    status: str

@app.post("/relayer/submit_permit/{prepared_id}", response_model=SubmitPermitResponse)
async def submit_relayer_permit(prepared_id: int, request: SubmitPermitRequest, db: Session = Depends(get_db)):
    """
    Submits a signed EIP-712 permit to the relayer for execution.
    (Currently mocked)
    """
    db_prepared_tx = db.query(models.PreparedTx).filter(models.PreparedTx.id == prepared_id).first()

    if not db_prepared_tx:
        raise HTTPException(status_code=404, detail="Prepared transaction not found")
    if db_prepared_tx.mode != 'relayer':
        raise HTTPException(status_code=400, detail="This endpoint is only for 'relayer' mode transactions.")
    if db_prepared_tx.status != 'PREPARED':
        raise HTTPException(status_code=400, detail=f"Transaction is not in 'PREPARED' state, but '{db_prepared_tx.status}'.")

    # This endpoint will now forward the request to the standalone relayer service.
    relayer_url = settings.RELAYER_URL
    if not relayer_url:
        raise HTTPException(status_code=500, detail="Relayer service URL is not configured.")

    relayer_payload = {
        "permit_payload": db_prepared_tx.payload,
        "signature": request.signature
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{relayer_url}/execute", json=relayer_payload) as response:
                if response.status != 200:
                    relayer_error = await response.text()
                    raise HTTPException(status_code=502, detail=f"Relayer service failed: {relayer_error}")

                relayer_response = await response.json()

                db_prepared_tx.status = 'SUBMITTED_TO_RELAYER'
                # Optionally, store the final tx_hash from the relayer
                # db_prepared_tx.final_tx_hash = relayer_response['tx_hash']
                db.commit()

                return {"relayer_tx_hash": relayer_response['tx_hash'], "status": "SUBMITTED_TO_RELAYER"}

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=503, detail=f"Could not connect to relayer service: {e}")
