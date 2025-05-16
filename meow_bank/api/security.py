from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from meow_bank.core.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Validate API key from header."""
    if api_key_header != settings.MEOW_BANK_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate API key",
        )

    return api_key_header
