"""
Database connection management.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from ..core.config import settings
from ..core.logging import get_logger
from ..core.exceptions import DatabaseConnectionError

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self):
        self.engine = None
        self.session_factory = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize database engine and session factory."""
        if self._initialized:
            logger.warning("database_already_initialized")
            return

        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                settings.database.connection_string,
                poolclass=QueuePool,
                pool_size=settings.database.pool_size,
                max_overflow=settings.database.max_overflow,
                pool_pre_ping=True,  # Verify connections before using
                echo=settings.debug,  # Log SQL queries in debug mode
            )

            # Add event listeners
            self._setup_event_listeners()

            # Create session factory
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )

            self._initialized = True
            logger.info("database_initialized", database=settings.database.name)

        except Exception as e:
            logger.error("database_initialization_failed", error=str(e))
            raise DatabaseConnectionError(f"Failed to initialize database: {e}")

    def _setup_event_listeners(self) -> None:
        """Set up SQLAlchemy event listeners for logging and monitoring."""

        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """Log database connections."""
            logger.debug("database_connection_established")

        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """Log connection checkout from pool."""
            logger.debug("database_connection_checked_out")

        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            """Log connection checkin to pool."""
            logger.debug("database_connection_checked_in")

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy Session instance

        Raises:
            DatabaseConnectionError: If database not initialized
        """
        if not self._initialized or not self.session_factory:
            raise DatabaseConnectionError("Database not initialized. Call initialize() first.")

        return self.session_factory()

    def close(self) -> None:
        """Close database connections and dispose of engine."""
        if self.engine:
            self.engine.dispose()
            logger.info("database_connections_closed")
            self._initialized = False


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection function for FastAPI.
    Yields a database session and ensures it's closed after use.

    Yields:
        SQLAlchemy Session

    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    if not db_manager._initialized:
        db_manager.initialize()

    session = db_manager.get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error("database_session_error", error=str(e))
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Initialize database (create tables if they don't exist).
    Should only be used in development or for initial setup.
    """
    from .base import Base
    from .models import (
        AuditLog, Policy, Whitelist, Blacklist,
        ApprovalRequest, EmailHistory, Metric
    )

    if not db_manager._initialized:
        db_manager.initialize()

    Base.metadata.create_all(bind=db_manager.engine)
    logger.info("database_tables_created")
