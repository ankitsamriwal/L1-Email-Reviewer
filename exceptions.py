"""
Custom exception classes for the L1 Email Release Agent.
"""


class L1AgentException(Exception):
    """Base exception for all L1 Agent errors."""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(L1AgentException):
    """Configuration or environment variable error."""
    pass


class ValidationError(L1AgentException):
    """Email validation error."""
    pass


class ManageEngineError(L1AgentException):
    """ManageEngine API error."""
    pass


class ManageEngineAuthError(ManageEngineError):
    """ManageEngine authentication failure."""
    pass


class ManageEngineRateLimitError(ManageEngineError):
    """ManageEngine rate limit exceeded."""
    pass


class ManageEngineNotFoundError(ManageEngineError):
    """ManageEngine resource not found."""
    pass


class ManageEngineTimeoutError(ManageEngineError):
    """ManageEngine API timeout."""
    pass


class ClaudeAPIError(L1AgentException):
    """Claude AI API error."""
    pass


class ClaudeRateLimitError(ClaudeAPIError):
    """Claude API rate limit exceeded."""
    pass


class ClaudeTimeoutError(ClaudeAPIError):
    """Claude API timeout."""
    pass


class DatabaseError(L1AgentException):
    """Database operation error."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Database connection failure."""
    pass


class RedisError(L1AgentException):
    """Redis cache error."""
    pass


class RedisConnectionError(RedisError):
    """Redis connection failure."""
    pass


class EmailParsingError(L1AgentException):
    """Email parsing or extraction error."""
    pass


class WorkflowError(L1AgentException):
    """LangGraph workflow execution error."""
    pass


class DomainValidationError(ValidationError):
    """Domain validation (SPF/DKIM/DMARC) error."""
    pass


class ContentAnalysisError(ValidationError):
    """Content analysis error."""
    pass


class SenderCheckError(ValidationError):
    """Sender verification error."""
    pass


class RulesEngineError(ValidationError):
    """Custom rules engine error."""
    pass


class ConfidenceScoringError(L1AgentException):
    """Confidence scoring calculation error."""
    pass


class ActionExecutionError(L1AgentException):
    """Action execution error."""
    pass


class NotificationError(L1AgentException):
    """Notification sending error."""
    pass


class AuditLoggingError(L1AgentException):
    """Audit logging error."""
    pass


class ExternalAPIError(L1AgentException):
    """External API (VirusTotal, Google Safe Browsing) error."""
    pass


class WhitelistBlacklistError(L1AgentException):
    """Whitelist/blacklist management error."""
    pass


class ApprovalWorkflowError(L1AgentException):
    """Approval workflow error."""
    pass
