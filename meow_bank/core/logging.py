import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

from .config import settings

log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"meow_bank_{datetime.now().strftime('%Y%m%d')}.log"

logger.remove()

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",  # noqa: E501
    level=settings.LOG_LEVEL,
)

logger.add(
    log_file,
    format="{message}",
    level="DEBUG",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    serialize=True,
)

log = logger
