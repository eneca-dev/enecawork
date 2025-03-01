import logging
import httpx

from supabase import Client
from app.schemas.auth import *
from app.exceptions.auth import *
from postgrest.exceptions import APIError
from app.utils.password_comparison import password_comparison


logger = logging.getLogger(__name__)

class AuthServices:

    @staticmethod
    def register_user(
        supabase: Client,
        first_name: str,
        last_name: str,
        department: str,
        team: str,
        position: str,
        category: str,
        email: str,
        password: str,
        password_confirm: str
    ) -> AuthRegisterResponse:
        try:
            if not password_comparison(password, password_confirm):
                raise PasswordMismatchException()

            # Check password complexity
            if len(password) < 6:
                raise WeakPasswordException()

            auth_response = supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'department': department,
                        'team': team,
                        'position': position,
                        'category': category
                    }
                }
            })

            if not auth_response.user:
                logger.error('Incomplete response from Supabase')
                raise AuthException(detail='Error creating user')

            return AuthRegisterResponse(
                first_name=auth_response.user.user_metadata.get('first_name'),
                last_name=auth_response.user.user_metadata.get('last_name'),
                department=auth_response.user.user_metadata.get('department'),
                team=auth_response.user.user_metadata.get('team'),
                position=auth_response.user.user_metadata.get('position'),
                category=auth_response.user.user_metadata.get('category'),
                email=auth_response.user.email
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitExceededException()
            if 'already registered' in str(e).lower():
                raise EmailAlreadyExistsException()
            raise AuthException(detail=str(e))

        except Exception as e:
            logger.error(f'Registration error: {str(e)}')
            raise AuthException(detail='Error registering user')

    @staticmethod
    def login_user(
        supabase: Client,
        email: str,
        password: str,
    ) -> AuthLoginResponse:
        try:
            auth_response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })

            if not auth_response.user:
                raise InvalidCredentialsException()

            if not auth_response.user.email_confirmed_at:
                raise EmailNotConfirmedException()

            return AuthLoginResponse(
                email=auth_response.user.email,
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitExceededException()
            if 'invalid credentials' in str(e).lower():
                raise InvalidCredentialsException()
            raise AuthException(detail=str(e))

        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            raise AuthException(detail='Error logging in')

    @staticmethod
    def reset_password(
        supabase: Client,
        email: str
    ) -> None:
        try:
            response = supabase.auth.reset_password_email(email)
            # TODO: add return object

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitExceededException()
            if 'timeout' in str(e).lower():
                raise SMTPException()
            raise AuthException(detail=str(e))

        except Exception as e:
            logger.error(f'Password reset error: {str(e)}')
            raise AuthException(detail='Error resetting password')

    @staticmethod
    def update_password(
        supabase: Client,
        access_token: str,
        refresh_token: str,
        password: str,
        password_confirm: str
    ) -> None:
        try:
            if not password_comparison(password, password_confirm):
                raise PasswordMismatchException()

            if len(password) < 6:
                raise WeakPasswordException()

            session = supabase.auth.set_session(access_token, refresh_token)
            
            update_response = supabase.auth.update_user(
                {
                    'password': password
                }
            )
            # TODO: add return object


        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise RateLimitExceededException()
            raise AuthException(detail=str(e))

        except Exception as e:
            logger.error(f'Password update error: {str(e)}')
            raise AuthException(detail='Error updating password')