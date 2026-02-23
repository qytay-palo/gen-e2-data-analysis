from loguru import logger
import os

class BaseConnection:
    """Base class for external data source connections."""
    def __init__(self, name: str):
        self.name = name

    def test_connection(self) -> bool:
        logger.info(f"Testing connection for {self.name}")
        # Implement connection test logic
        return True

    def connect(self):
        raise NotImplementedError("Connect method must be implemented by subclasses.")
