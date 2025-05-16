from fastapi import HTTPException


class ResourceNotFoundError(HTTPException):
    """Raised when a requested resource is not found."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ValidationError(HTTPException):
    """Raised when there is a validation error."""

    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class BusinessLogicError(HTTPException):
    """Raised when there is a business logic error."""

    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
