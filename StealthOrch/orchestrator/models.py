import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Opportunity(Base):
    __tablename__ = 'opportunities'
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, nullable=False)
    contract_address = Column(String, nullable=False)
    function_name = Column(String, nullable=False)
    args = Column(JSON)
    chain = Column(String, nullable=False)
    evidence = Column(String)
    priority = Column(Integer, default=0)
    detected_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='new', index=True) # e.g., 'new', 'prepared', 'executed', 'failed'

    prepared_txs = relationship("PreparedTx", back_populates="opportunity")

class PreparedTx(Base):
    __tablename__ = 'prepared_txs'
    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    mode = Column(String, nullable=False) # 'wc', 'safe', 'relayer'
    payload = Column(JSON, nullable=False)
    payload_hash = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, default='PREPARED', index=True) # 'PREPARED', 'SIGNED', 'EXECUTED', 'FAILED'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    opportunity = relationship("Opportunity", back_populates="prepared_txs")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    actor = Column(String, default='system')
    action = Column(String, nullable=False) # e.g., 'prepare_tx', 'approve_tx'
    outcome = Column(String, nullable=False) # 'success', 'failure'
    details = Column(JSON)
