from fastapi import HTTPException

class AuthException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail=detail
        )

class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail='Invalid credentials'
        )

class EmailAlreadyExistsException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='User with this email already exists'
        )

class PasswordMismatchException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='Passwords do not match'
        )

class WeakPasswordException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='Password is too simple. Use at least 6 characters, including letters and numbers'
        )

class EmailNotConfirmedException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail='Email is not confirmed'
        )

class RateLimitExceededException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=429,
            detail='Rate limit exceeded. Please wait a few minutes'
        )

class SMTPException(AuthException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail='Error sending email. Please try again later'
        )