# This file is responsible for signing , encoding , decoding and returning JWTS
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
import jwt

from settings.database_config.config import ALGORITHM, SECRET


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
              'steam_id': data['steam_id']}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)


def create_refresh_token(data):
    encode = {'sub': data['email'], 'id': data['id'], 'username': data['username'], 'user_role': data['user_role'],
              'steam_id': data['steam_id']}
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
        steam_id: str = payload.get('steam_id')
        return {
            'email': email,
            'id': id,
            'user_role': user_role,
            'username': username,
            'steam_id': steam_id
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials")