"""
Structured logging configuration using structlog.
"""

import logging
import sys
from typing import Any, Dict
import structlog
from structlog.types import EventDict, Processor

from .config import settings


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to all log entries."""
    event_dict["app"] = "l1-email-agent"
    event_dict["environment"] = settings.environment
    return event_dict


def censor_sensitive_data(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Censor sensitive data from logs (API keys, passwords, etc.)."""
    sensitive_keys = ["password", "api_key", "token", "secret", "auth"]

    for key in list(event_dict.keys()):
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            event_dict[key] = "***REDACTED***"

    return event_dict


def setup_logging() -> None:
    """
    Configure structlog for structured logging.
    Sets up processors, formatters, and output handlers.
    """
    # Shared processors for all configurations
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        add_app_context,
        censor_sensitive_data,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Configure structlog
    if settings.is_development:
        # Development: Use console renderer with colors
        structlog.configure(
            processors=shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True)
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Production: Use JSON renderer for log aggregation
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Set log levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LoggerAdapter:
    """
    Adapter to provide additional context to logs within a specific scope.
    Usage:
        with LoggerAdapter(logger, email_id="12345"):
            logger.info("processing_email")
    """

    def __init__(self, logger: structlog.stdlib.BoundLogger, **context: Any):
        self.logger = logger
        self.context = context
        self.token = None

    def __enter__(self) -> structlog.stdlib.BoundLogger:
        """Enter context and bind additional data."""
        self.token = structlog.contextvars.bind_contextvars(**self.context)
        return self.logger

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and clear bound data."""
        if self.token:
            structlog.contextvars.unbind_contextvars(*self.context.keys())


# Initialize logging on module import
setup_logging()
