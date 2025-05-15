import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

from .config import settings

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Generate log file name with timestamp
log_file = log_dir / f"meow_bank_{datetime.now().strftime('%Y%m%d')}.log"

# Remove default logger
logger.remove()

# Add console logger with color
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",  # noqa: E501
    level=settings.LOG_LEVEL,
)

# Add file logger with JSON format
logger.add(
    log_file,
    format="{message}",
    level="DEBUG",  # Always log DEBUG to file
    rotation="1 day",
    retention="30 days",
    compression="zip",
    serialize=True,  # This will automatically serialize the log record to JSON
)

# Export logger instance
log = logger
