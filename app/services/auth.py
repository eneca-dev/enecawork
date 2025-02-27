from supabase import Client
from app.schemas.auth import *
from fastapi import HTTPException
import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)

class Auth:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    async def register_user(
        self,
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
            if password != password_confirm:
                raise HTTPException(
                    status_code=400,
                    detail='Пароли не совпадают'
                )

            logger.info(f"Attempting to register user with email: {email}")
            
            auth_response = self.supabase.auth.sign_up({
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
            
            logger.info(f"Supabase response received: {auth_response}")
            
            if not auth_response.user or not auth_response.session:
                logger.error("Incomplete response from Supabase")
                raise HTTPException(
                    status_code=400,
                    detail='Неполный ответ от сервера аутентификации'
                )

            return AuthRegisterResponse(
                first_name=auth_response.user.user_metadata.get('first_name'),
                last_name=auth_response.user.user_metadata.get('last_name'),
                department=auth_response.user.user_metadata.get('department'),
                team=auth_response.user.user_metadata.get('team'),
                position=auth_response.user.user_metadata.get('position'),
                category=auth_response.user.user_metadata.get('category'),
                email=auth_response.user.email,
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token
            )

        except Exception as e:
            logger.error(f'Registration error: {str(e)}')
            logger.error(f'Error type: {type(e)}')
            if hasattr(e, 'message'):
                logger.error(f'Error message: {e.message}')
            raise HTTPException(
                status_code=400,
                detail=f'Ошибка при регистрации: {str(e)}'
            )

    async def login_user(
        self,
        email: str,
        password: str,
    ) -> AuthLoginResponse:
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })

            return AuthLoginResponse(
                email=auth_response.user.email,
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token
            )
        except Exception as e:
            print(f'Login error: {str(e)}')
            raise HTTPException(status_code=401, detail='Неверные учетные данные')