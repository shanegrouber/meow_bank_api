from typing import Annotated

from pydantic import StringConstraints

UUID_PATTERN = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
UUIDStr = Annotated[str, StringConstraints(pattern=UUID_PATTERN)]
