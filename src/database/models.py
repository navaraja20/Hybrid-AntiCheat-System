"""SQLAlchemy ORM models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    """Player information."""
    __tablename__ = "players"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_sessions = Column(Integer, default=0)
    total_playtime = Column(Float, default=0.0)
    status = Column(String, default="clean")  # clean, flagged, banned, shadow_banned
    

class DetectionEvent(Base):
    """Detection events for audit trail."""
    __tablename__ = "detection_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String, nullable=False)  # rule_violation, anomaly, ban, etc.
    severity = Column(Float)
    features = Column(JSON)
    details = Column(JSON)
    

class Ban(Base):
    """Ban records."""
    __tablename__ = "bans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False, index=True)
    banned_at = Column(DateTime, default=datetime.utcnow)
    ban_type = Column(String, nullable=False)  # permanent, shadow, temporary
    reason = Column(String)
    evidence = Column(JSON)
    confidence_score = Column(Float)
    reviewed = Column(Boolean, default=False)
    appeal_status = Column(String, default=None)  # None, pending, approved, rejected


class ReviewCase(Base):
    """Cases pending human review."""
    __tablename__ = "review_cases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=0)  # Higher = more urgent
    status = Column(String, default="pending")  # pending, reviewed, escalated
    cheat_score = Column(Float)
    features = Column(JSON)
    reviewer_id = Column(String, default=None)
    verdict = Column(String, default=None)  # clean, ban, shadow_ban
    reviewed_at = Column(DateTime, default=None)
    notes = Column(String, default=None)