from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
import functools
from contextlib import suppress
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import config
import models


ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = config.settings.refresh_token_expire_minutes
ALGORITHM = config.settings.algorithm
JWT_SECRET_KEY = config.settings.jwt_secret_key
JWT_REFRESH_SECRET_KEY = config.settings.jwt_refresh_secret_key

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def validate_password(password: str) -> bool:
    """
    Validates the strength of the provided password.

    Args:
        password: The password to validate.

    Returns:
        True if the password is strong, False otherwise.
    """

    # Check minimum password length
    if len(password) < 8:
        return False

    # Check for uppercase letters
    if not any(c.isupper() for c in password):
        return False

    # Check for lowercase letters
    if not any(c.islower() for c in password):
        return False

    # Check for digits
    if not any(c.isdigit() for c in password):
        return False

    # Additional checks for special characters, word lists, etc. can be added here

    return True


def create_access_token(subject: Union[str, Any], expires_delta: int  = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY,ALGORITHM)
        return payload
    except InvalidTokenError:
        return None

def token_required(secret_key, algorithm):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Retrieve token from a more conventional location (e.g., headers)
                token = kwargs.get('Authorization', '').split(' ')[1]  # Example header retrieval

                # Decode and validate token
                payload = jwt.decode(token, secret_key = JWT_SECRET_KEY, algorithms= ALGORITHM)
                user_id = payload['sub']

                # Query for token status
                with kwargs['session'].begin():
                    token_data = kwargs['session'].query(models.Token) \
                        .filter_by(user_id=user_id, access_token=token, status=True) \
                        .first()

                if token_data:
                    return func(*args, **kwargs)
                else:
                    raise ValueError("Invalid or blocked token")  # More specific exception

            except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
                raise ValueError("Invalid token") from e
            except ValueError as e:
                return {'msg': str(e)}, 401  # Return informative error response
            except Exception as e:  # Catch other potential errors
                raise ValueError("Internal server error") from e

        return wrapper

    return decorator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

jwt_bearer = JWTBearer()