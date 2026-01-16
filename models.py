"""
SQLAlchemy ORM models for database tables.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Text, JSON,
    Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.sql import func

from .base import Base, TimestampMixin


class AuditLog(Base, TimestampMixin):
    """Audit logs for email review actions."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=func.now(), index=True)

    # Email information
    email_subject = Column(Text)
    sender = Column(String(255), index=True)
    recipient = Column(String(255))
    sender_domain = Column(String(255), index=True)
    sender_ip = Column(INET)

    # Validation scores
    domain_validation_score = Column(Float)
    domain_validation_details = Column(JSONB)
    content_analysis_score = Column(Float)
    content_analysis_details = Column(JSONB)
    sender_check_score = Column(Float)
    sender_check_details = Column(JSONB)
    rules_evaluation_score = Column(Float)
    rules_evaluation_details = Column(JSONB)

    # Confidence and decision
    overall_confidence_score = Column(Float, nullable=False)
    risk_level = Column(String(20))
    decision = Column(String(50), nullable=False, index=True)
    decision_reason = Column(Text)

    # Action taken
    action_taken = Column(String(50))
    action_timestamp = Column(DateTime)
    action_result = Column(JSONB)

    # Performance tracking
    processing_duration_ms = Column(Integer)

    # Metadata
    metadata = Column(JSONB)

    __table_args__ = (
        Index('idx_audit_timestamp_decision', 'timestamp', 'decision'),
        Index('idx_audit_sender_domain', 'sender_domain'),
    )


class Policy(Base, TimestampMixin):
    """Custom rules and policies."""

    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(Integer, nullable=False, index=True)
    rule_type = Column(String(50), nullable=False)
    condition = Column(JSONB, nullable=False)
    action = Column(JSONB, nullable=False)
    enabled = Column(Boolean, default=True, index=True)

    __table_args__ = (
        Index('idx_policy_priority_enabled', 'priority', 'enabled'),
    )


class Whitelist(Base, TimestampMixin):
    """Whitelist entries for trusted senders/domains/IPs."""

    __tablename__ = "whitelists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_type = Column(String(20), nullable=False)  # 'domain', 'email', 'ip'
    value = Column(String(255), nullable=False)
    added_by = Column(String(255))
    reason = Column(Text)

    __table_args__ = (
        UniqueConstraint('entry_type', 'value', name='uq_whitelist_type_value'),
        Index('idx_whitelist_type_value', 'entry_type', 'value'),
    )


class Blacklist(Base, TimestampMixin):
    """Blacklist entries for malicious senders/domains/IPs."""

    __tablename__ = "blacklists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_type = Column(String(20), nullable=False)  # 'domain', 'email', 'ip'
    value = Column(String(255), nullable=False)
    added_by = Column(String(255))
    reason = Column(Text)

    __table_args__ = (
        UniqueConstraint('entry_type', 'value', name='uq_blacklist_type_value'),
        Index('idx_blacklist_type_value', 'entry_type', 'value'),
    )


class ApprovalRequest(Base, TimestampMixin):
    """Approval requests for medium-confidence emails."""

    __tablename__ = "approval_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(String(255), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True, default='pending')
    approver_email = Column(String(255), nullable=False)
    confidence_score = Column(Float)
    context = Column(JSONB)
    expires_at = Column(DateTime)
    reviewed_at = Column(DateTime)
    review_notes = Column(Text)

    __table_args__ = (
        Index('idx_approval_status_created', 'status', 'created_at'),
    )


class EmailHistory(Base, TimestampMixin):
    """Historical email data for sender reputation."""

    __tablename__ = "email_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender = Column(String(255), nullable=False, index=True)
    sender_domain = Column(String(255), nullable=False, index=True)
    recipient = Column(String(255))
    timestamp = Column(DateTime, nullable=False, index=True)
    was_released = Column(Boolean)
    confidence_score = Column(Float)

    __table_args__ = (
        Index('idx_email_history_sender_timestamp', 'sender', 'timestamp'),
        Index('idx_email_history_domain_timestamp', 'sender_domain', 'timestamp'),
    )


class Metric(Base):
    """System performance metrics."""

    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    labels = Column(JSONB)
    timestamp = Column(DateTime, nullable=False, default=func.now(), index=True)

    __table_args__ = (
        Index('idx_metric_name_timestamp', 'metric_name', 'timestamp'),
    )
