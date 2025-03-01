from pydantic import BaseModel, EmailStr

class AuthRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    department: str
    team: str = 'general'
    position: str
    category: str = 'general'
    email: EmailStr
    password: str
    password_confirm: str
    
class AuthRegisterResponse(BaseModel):
    first_name: str
    last_name: str
    department: str
    team: str = 'general'
    position: str
    category: str = 'general'
    email: EmailStr

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthLoginResponse(BaseModel):
    email: EmailStr
    access_token: str
    refresh_token: str

class AuthResetPasswordRequest(BaseModel):
    email: EmailStr

class AuthUpdatePasswordRequest(BaseModel):
    access_token: str
    refresh_token: str
    password: str
    password_confirm: str