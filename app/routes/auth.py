from supabase import Client
from app.schemas.auth import *
from app.services.auth import AuthServices
from app.database import get_supabase
from fastapi import APIRouter, Depends

auth_router = APIRouter()

@auth_router.post('/register')
def register(
    user_data: AuthRegisterRequest,
    supabase: Client = Depends(get_supabase)
) -> AuthRegisterResponse:

    result = AuthServices().register_user(supabase=supabase, **user_data.model_dump())
    return result


@auth_router.post('/login')
def login(
    user_data: AuthLoginRequest,
    supabase: Client = Depends(get_supabase)
) -> AuthLoginResponse:

    result = AuthServices().login_user(supabase=supabase, **user_data.model_dump())
    return result


@auth_router.post('/reset-password')
def reset_password(
    user_data: AuthResetPasswordRequest,
    supabase: Client = Depends(get_supabase)
) -> None:

    result = AuthServices().reset_password(supabase=supabase, **user_data.model_dump())
    return result


@auth_router.post('/update-password')
def update_password(
    user_data: AuthUpdatePasswordRequest,
    supabase: Client = Depends(get_supabase)
) -> None:
    
    result = AuthServices().update_password(supabase=supabase, **user_data.model_dump())
    return result