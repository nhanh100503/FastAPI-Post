from fastapi import status, Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Callable, Any, Type


# ==== 1. Custom Exception Base ====
class CustomException(Exception):
    pass

# ==== 2. Custom Exceptions ====
class InvalidToken(CustomException): pass
class InvalidUserToken(CustomException): pass
# class RevokedToken(CustomException): pass
# class AccessTokenRequired(CustomException): pass
# class RefreshTokenRequired(CustomException): pass
# class InvalidCredentials(CustomException): pass
# class InsufficientPermission(CustomException): pass
# class AccountNotVerified(CustomException): pass
class UserAlreadyExists(CustomException): pass
class PostNotFound(CustomException): pass
class UserNotFound(CustomException): pass
class EmailNotFound(CustomException): pass
class InvalidPassword(CustomException): pass
class ExpiredToken(CustomException): pass


# ==== 3. Handler Factory ====
def create_exception_handler(status_code: int, detail: dict) -> Callable:
    async def handler(request: Request, exc: Exception):
        return JSONResponse(content=detail, status_code=status_code)
    return handler


# ==== 4. Exception Mapping ====
EXCEPTION_HANDLERS: list[tuple[Type[Exception], int, dict[str, Any]]] = [
    (UserAlreadyExists, status.HTTP_403_FORBIDDEN, {
        "message": "User with email already exists",
        "error_code": "user_exists"
    }),
    (UserNotFound, status.HTTP_404_NOT_FOUND, {
        "message": "User not found",
        "error_code": "user_not_found"
    }),
    (PostNotFound, status.HTTP_404_NOT_FOUND, {
        "message": "Post not found",
        "error_code": "post_not_found"
    }),
    (EmailNotFound, status.HTTP_404_NOT_FOUND, {
        "message": "Email not found",
        "error_code": "email_not_found"
    }),
    (InvalidPassword, status.HTTP_401_UNAUTHORIZED, {
        "message": "Incorrect password",
        "error_code": "invalid_password"
    }),
    # (InvalidCredentials, status.HTTP_400_BAD_REQUEST, {
    #     "message": "Invalid Email Or Password",
    #     "error_code": "invalid_email_or_password"
    # }),
    (InvalidToken, status.HTTP_401_UNAUTHORIZED, {
        "message": "Token is invalid",
        "error_code": "invalid_token"
    }),
    (InvalidUserToken, status.HTTP_401_UNAUTHORIZED, {
        "message": "Invalid token: user data missing",
        "error_code": "invalid_user_token"
    }),
    (ExpiredToken, status.HTTP_401_UNAUTHORIZED, {
        "message": "Token is expired",
        "error_code": "expired_token"
    }),
    # (RevokedToken, status.HTTP_401_UNAUTHORIZED, {
    #     "message": "Token has been revoked",
    #     "resolution": "Please get a new token",
    #     "error_code": "token_revoked"
    # }),
    # (AccessTokenRequired, status.HTTP_401_UNAUTHORIZED, {
    #     "message": "Access token required",
    #     "error_code": "access_token_required"
    # }),
    # (RefreshTokenRequired, status.HTTP_403_FORBIDDEN, {
    #     "message": "Refresh token required",
    #     "error_code": "refresh_token_required"
    # }),
    # (InsufficientPermission, status.HTTP_403_FORBIDDEN, {
    #     "message": "Insufficient permissions",
    #     "error_code": "insufficient_permissions"
    # }),
    # (TagNotFound, status.HTTP_404_NOT_FOUND, {
    #     "message": "Tag not found",
    #     "error_code": "tag_not_found"
    # }),
    # (TagAlreadyExists, status.HTTP_403_FORBIDDEN, {
    #     "message": "Tag already exists",
    #     "error_code": "tag_exists"
    # }),
    # (AccountNotVerified, status.HTTP_403_FORBIDDEN, {
    #     "message": "Account not verified",
    #     "error_code": "account_not_verified",
    #     "resolution": "Please verify your email"
    # }),
]


# ==== 5. Register All Handlers ====
def register_all_errors(app: FastAPI):
    for exc_class, status_code, detail in EXCEPTION_HANDLERS:
        app.add_exception_handler(exc_class, create_exception_handler(status_code, detail))

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "error_code": "server_error"
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def db_error_handler(request: Request, exc: SQLAlchemyError):
        print(f"Database Error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database operation failed",
                "error_code": "db_error"
            },
        )

