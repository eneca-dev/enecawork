from supabase import Client
from app.schemas.auth import *
from app.services.auth import Auth
from app.database import get_supabase
from fastapi import APIRouter, Depends, HTTPException
import logging

logger = logging.getLogger(__name__)

auth_router = APIRouter()

@auth_router.post('/register')
async def register(
    user_data: AuthRegisterRequest,
    supabase: Client = Depends(get_supabase)
) -> AuthRegisterResponse:

    logger.info(f"Received registration request for email: {user_data.email}")
    service = Auth(supabase)
    result = await service.register_user(**user_data.model_dump())
    logger.info("Registration successful")
    return result

@auth_router.post('/login')
async def login(
    user_data: AuthLoginRequest,
    supabase: Client = Depends(get_supabase)
) -> AuthLoginResponse:
    try:
        service = Auth(supabase)
        result = await service.login_user(**user_data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail='Неверные учетные данные'
        )