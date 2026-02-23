"""Logging setup utility."""
from loguru import logger
import sys
from pathlib import Path


def setup_logger(log_name: str, log_dir: str = "logs/etl") -> None:
    """
    Configure loguru logger with file and console output.
    
    Args:
        log_name: Name of the log file (without extension)
        log_dir: Directory to save logs
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Remove default logger
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO"
    )
    
    # Add file handler
    logger.add(
        log_path / f"{log_name}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days"
    )
    
    logger.info(f"Logger initialized: {log_name}")
