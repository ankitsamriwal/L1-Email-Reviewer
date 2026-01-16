"""
Core configuration management using Pydantic Settings.
Loads configuration from environment variables and .env file.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ManageEngineConfig(BaseSettings):
    """ManageEngine ServiceDesk Plus API configuration."""

    base_url: str = Field(..., alias="MANAGEENGINE_BASE_URL")
    api_key: str = Field(..., alias="MANAGEENGINE_API_KEY")
    on_hold_status: str = Field("On Hold", alias="MANAGEENGINE_ON_HOLD_STATUS")
    released_status: str = Field("Open", alias="MANAGEENGINE_RELEASED_STATUS")
    timeout: int = Field(30, alias="MANAGEENGINE_TIMEOUT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ClaudeConfig(BaseSettings):
    """Claude AI API configuration."""

    api_key: str = Field(..., alias="CLAUDE_API_KEY")
    model: str = Field("claude-sonnet-4-5-20250929", alias="CLAUDE_MODEL")
    max_tokens: int = Field(4096, alias="CLAUDE_MAX_TOKENS")
    temperature: float = Field(0.0, alias="CLAUDE_TEMPERATURE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseConfig(BaseSettings):
    """PostgreSQL database configuration."""

    host: str = Field("localhost", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")
    name: str = Field("l1_agent", alias="DB_NAME")
    user: str = Field("l1_user", alias="DB_USER")
    password: str = Field(..., alias="DB_PASSWORD")
    pool_size: int = Field(20, alias="DB_POOL_SIZE")
    max_overflow: int = Field(10, alias="DB_MAX_OVERFLOW")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def connection_string(self) -> str:
        """Generate PostgreSQL connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseSettings):
    """Redis cache configuration."""

    host: str = Field("localhost", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
    password: Optional[str] = Field(None, alias="REDIS_PASSWORD")
    db: int = Field(0, alias="REDIS_DB")
    cache_ttl: int = Field(3600, alias="REDIS_CACHE_TTL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SMTPConfig(BaseSettings):
    """SMTP email configuration."""

    host: str = Field("smtp.gmail.com", alias="SMTP_HOST")
    port: int = Field(587, alias="SMTP_PORT")
    username: str = Field(..., alias="SMTP_USERNAME")
    password: str = Field(..., alias="SMTP_PASSWORD")
    from_address: str = Field(..., alias="SMTP_FROM_ADDRESS")
    from_name: str = Field("L1 Email Release Agent", alias="SMTP_FROM_NAME")
    use_tls: bool = Field(True, alias="SMTP_USE_TLS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class NotificationConfig(BaseSettings):
    """Notification recipients configuration."""

    approval_recipients: str = Field(..., alias="APPROVAL_RECIPIENTS")
    escalation_recipients: str = Field(..., alias="ESCALATION_RECIPIENTS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def approval_emails(self) -> List[str]:
        """Parse approval recipients into list."""
        return [email.strip() for email in self.approval_recipients.split(",")]

    @property
    def escalation_emails(self) -> List[str]:
        """Parse escalation recipients into list."""
        return [email.strip() for email in self.escalation_recipients.split(",")]


class SecurityConfig(BaseSettings):
    """Security and authentication configuration."""

    api_key: str = Field(..., alias="API_KEY")
    rate_limit_per_minute: int = Field(100, alias="RATE_LIMIT_PER_MINUTE")
    allowed_ip_ranges: str = Field("", alias="ALLOWED_IP_RANGES")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_ip_list(self) -> List[str]:
        """Parse allowed IP ranges into list."""
        if not self.allowed_ip_ranges:
            return []
        return [ip.strip() for ip in self.allowed_ip_ranges.split(",")]


class SchedulerConfig(BaseSettings):
    """Background scheduler configuration."""

    enabled: bool = Field(True, alias="SCHEDULER_ENABLED")
    poll_interval: int = Field(300, alias="SCHEDULER_POLL_INTERVAL")  # seconds
    batch_size: int = Field(50, alias="SCHEDULER_BATCH_SIZE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ThresholdsConfig(BaseSettings):
    """Confidence thresholds for decision making."""

    auto_release_min: float = Field(0.85, alias="CONFIDENCE_AUTO_RELEASE_MIN")
    approval_min: float = Field(0.60, alias="CONFIDENCE_APPROVAL_MIN")
    escalate_max: float = Field(0.60, alias="CONFIDENCE_ESCALATE_MAX")
    hold_extension_default: int = Field(7, alias="HOLD_EXTENSION_DEFAULT")
    hold_extension_high_risk: int = Field(30, alias="HOLD_EXTENSION_HIGH_RISK")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("auto_release_min", "approval_min", "escalate_max")
    @classmethod
    def validate_confidence_range(cls, v: float) -> float:
        """Ensure confidence thresholds are between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Confidence threshold must be between 0 and 1")
        return v


class ExternalAPIsConfig(BaseSettings):
    """External API keys (optional)."""

    virustotal_api_key: Optional[str] = Field(None, alias="VIRUSTOTAL_API_KEY")
    google_safe_browsing_api_key: Optional[str] = Field(None, alias="GOOGLE_SAFE_BROWSING_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Main application settings."""

    environment: str = Field("development", alias="ENVIRONMENT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    debug: bool = Field(False, alias="DEBUG")

    # Sub-configurations
    manageengine: ManageEngineConfig = Field(default_factory=ManageEngineConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)
    notification: NotificationConfig = Field(default_factory=NotificationConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    thresholds: ThresholdsConfig = Field(default_factory=ThresholdsConfig)
    external_apis: ExternalAPIsConfig = Field(default_factory=ExternalAPIsConfig)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency injection function for FastAPI.
    Returns the global settings instance.
    """
    return settings
