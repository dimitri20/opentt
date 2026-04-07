from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class NotFoundException(HTTPException):
    """Exception raised when a resource is not found"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException(HTTPException):
    """Exception raised when there is a conflict (e.g., duplicate resource)"""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ValidationException(HTTPException):
    """Exception raised for business logic validation errors"""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ForbiddenException(HTTPException):
    """Exception raised when user doesn't have permission"""

    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    """Handler for NotFoundException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "not_found"},
    )


async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    """Handler for ConflictException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "conflict"},
    )


async def validation_exception_handler(
    request: Request, exc: ValidationException
) -> JSONResponse:
    """Handler for ValidationException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "validation_error"},
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    """Handler for ForbiddenException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "forbidden"},
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handler for Pydantic validation errors"""
    errors = exc.errors()
    formatted_errors = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in errors
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": formatted_errors, "error": "validation_error"},
    )
