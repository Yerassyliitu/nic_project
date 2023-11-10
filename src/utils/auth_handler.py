# This file is responsible for signing , encoding , decoding and returning JWTS
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException

from passlib.context import CryptContext
import jwt

from src.models.auth import RevokedToken
from settings.database_config.config import ALGORITHM, SECRET
from fastapi.security import OAuth2PasswordBearer
from settings.database_connection.connection import async_session
from sqlalchemy.future import select

JWT_SECRET = SECRET
JWT_ALGORITHM = ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')




def token_response(token: str):
    return {
        "access_token": token
    }


# function used for signing the JWT string
# old_data = (email: str, id: int, username: str, organization_id: int, organization_role: str, expires_delta: timedelta)
def create_access_token(data, expires_delta=timedelta(minutes=20)):
    encode = {'sub': data['email'], 'id': data['id'], 'username': data['username'], 'user_role': data['user_role'],
              'organization_id': data['organization_id'], 'organization_role': data['organization_role']}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)


def create_refresh_token(data):
    encode = {'sub': data['email'], 'id': data['id'], 'username': data['username'], 'user_role': data['user_role'],
              'organization_id': data['organization_id'], 'organization_role': data['organization_role']}
    expires = datetime.utcnow() + timedelta(minutes=14400)
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)


def decode_token(token, secret_key=SECRET, algorithm=ALGORITHM):
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    return payload


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # decode token and extract username and expires data
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        username: str = payload.get('username')
        id: int = payload.get('id')
        user_role: int = payload.get('user_role')
        organization_id: int = payload.get('organization_id')
        organization_role: str = payload.get('organization_role')
        async with async_session() as session:
            result = await session.execute(select(RevokedToken).filter(RevokedToken.jti == token))
            if_token_revoked = result.scalar_one_or_none()
            if if_token_revoked:
                raise HTTPException(status_code=401, detail="Unauthorized")
        return {
            'email': email,
            'id': id,
            'user_role': user_role,
            'username': username,
            'organization_id': organization_id,
            'organization_role': organization_role
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

