from fastapi.exceptions import HTTPException
from fastapi import status, Header
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from datetime import timedelta, datetime, timezone
from typing import Annotated

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
# REFRESH_TOKEN_EXPIRE_MINUTES = 99999999

def create_access_token(data: dict):
    access_token_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_encode.update({"exp": expire})
    access_token = jwt.encode(access_token_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def create_refresh_token(data: dict):
    refresh_token_encode = data.copy()
    refresh_token = jwt.encode(refresh_token_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token

# def check_token_validation(token: str):
def check_access_token_validation(access_token: Annotated[str, Header()]):
    token = access_token.split()

    if token[0] == 'Bearer' and len(token) == 2:
        token = token[1]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Please insert Bearer before Token!!'
        )
    try:
        # Decode the token
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_data.get('exp'):
            return {
                'username': decoded_data.get('sub')
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is not valid for Login!!"
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired!!"
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token Invalid!!"
            )

def check_refresh_token_validation(refresh_token: Annotated[str, Header()]):
    token = refresh_token.split()
    
    if token[0] == 'Bearer' and len(token) == 2:
        token = token[1]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Please insert Bearer before Token!!'
        )
    try:
        # Decode the token
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_data.get('exp'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token is not valid for refresh token!!"
            )
        else:
            return create_access_token(decoded_data)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid refresh token!!"
            )