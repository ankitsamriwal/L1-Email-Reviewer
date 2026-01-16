"""
System constants and enumerations.
"""

from enum import Enum


class DecisionType(str, Enum):
    """Email review decision types."""
    AUTO_RELEASE = "auto_release"
    APPROVAL_REQUIRED = "approval_required"
    ESCALATE = "escalate"


class RiskLevel(str, Enum):
    """Risk level classifications."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApprovalStatus(str, Enum):
    """Approval request statuses."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class EmailStatus(str, Enum):
    """Email processing statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ActionType(str, Enum):
    """Action types for email handling."""
    RELEASE = "release"
    KEEP_QUARANTINED = "keep_quarantined"
    CREATE_APPROVAL = "create_approval"
    ADD_NOTE = "add_note"


class ValidationComponent(str, Enum):
    """Validation component names."""
    DOMAIN = "domain_validation"
    CONTENT = "content_analysis"
    SENDER = "sender_check"
    RULES = "rules_evaluation"


class RuleType(str, Enum):
    """Custom rule types."""
    CONTENT = "content"
    SENDER = "sender"
    ATTACHMENT = "attachment"
    TIME_BASED = "time_based"
    VOLUME = "volume"


class WhitelistType(str, Enum):
    """Whitelist/blacklist entry types."""
    DOMAIN = "domain"
    EMAIL = "email"
    IP = "ip"


# Scoring weights (can be overridden by config)
DEFAULT_SCORING_WEIGHTS = {
    "domain_validation": 0.30,
    "content_analysis": 0.35,
    "sender_check": 0.25,
    "rules_evaluation": 0.10,
}

# Component sub-weights
COMPONENT_WEIGHTS = {
    "domain": {
        "spf": 0.25,
        "dkim": 0.25,
        "dmarc": 0.20,
        "reputation": 0.20,
        "dnsbl": 0.10,
    },
    "content": {
        "phishing": 0.40,
        "spam": 0.25,
        "url_safety": 0.25,
        "attachments": 0.10,
    },
    "sender": {
        "whitelist": 0.40,
        "blacklist": 0.30,
        "history": 0.20,
        "relationship": 0.10,
    },
}

# Phishing indicators keywords
PHISHING_KEYWORDS = [
    "urgent", "immediate action", "verify now", "suspended account",
    "confirm identity", "click here", "update payment", "security alert",
    "unusual activity", "account locked", "expire", "limited time",
]

# Spam indicators keywords
SPAM_KEYWORDS = [
    "free", "winner", "congratulations", "act now", "limited offer",
    "click here", "buy now", "discount", "promotion", "prize",
]

# Suspicious attachment extensions
SUSPICIOUS_EXTENSIONS = [
    ".exe", ".bat", ".cmd", ".scr", ".pif", ".vbs", ".js",
    ".jar", ".com", ".msi", ".dll", ".hta", ".cpl",
]

# Allowed attachment extensions (if using whitelist approach)
ALLOWED_EXTENSIONS = [
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".txt", ".csv", ".zip", ".png", ".jpg", ".jpeg", ".gif",
]

# Default cache keys
CACHE_KEYS = {
    "processed_emails": "l1:processed:email:{}",
    "sender_history": "l1:sender:history:{}",
    "domain_reputation": "l1:domain:reputation:{}",
    "url_safety": "l1:url:safety:{}",
}

# API rate limits
RATE_LIMITS = {
    "manageengine": 60,  # requests per minute
    "claude": 50,  # requests per minute
    "virustotal": 4,  # requests per minute (free tier)
}

# Timeouts (seconds)
TIMEOUTS = {
    "manageengine_api": 30,
    "claude_api": 60,
    "external_api": 15,
    "database_query": 10,
}

# Retry configuration
RETRY_CONFIG = {
    "max_attempts": 3,
    "backoff_factor": 2,
    "max_backoff": 30,
}

# Log file paths
LOG_PATHS = {
    "application": "logs/l1-agent.log",
    "audit": "logs/audit.log",
    "error": "logs/error.log",
}
