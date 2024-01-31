from typing import Annotated,Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import DecodeError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
import models, schemas
import utils 
import config 
from pydantic import EmailStr


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login",
                                     scheme_name="JWT")

def get_user(db: Session, user_id: int) -> schemas.UserOut:
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        user_out = schemas.UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            fullname=user.fullname,
            is_active=user.is_active,
        )
        return user_out
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_user_by_username(db: Session, username: str):
    username_data = db.query(models.User).filter(models.User.username == username).first()
    if username_data:
        user_dict = {
            "id": username_data.id,
            "fullname": username_data.fullname,
            "email": username_data.email,
            "is_active": username_data.is_active,
        }
        return schemas.UserOut(**user_dict)

def get_user_by_email(db: Session, email: EmailStr) -> schemas.User:
    user_data = db.query(models.User).filter(models.User.email == email).first()
    if user_data:
        user = schemas.User(
            id=user_data.id,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            fullname=user_data.fullname,
            is_active=user_data.is_active,
            createdAt=user_data.createdAt,
            updatedAt=user_data.updatedAt,
        )
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    db.delete(user)
    db.commit()

    return {"status": "success", "message": f"User with id {user_id} deleted"}

     
def authenticate_user(db: Session,email: str, password: str):
    user = get_user_by_email(db,email)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_current_user(db:Session,token: str = Depends(oauth2_scheme)) -> schemas.UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.settings.jwt_secret_key, algorithms=[config.settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except DecodeError:
        raise credentials_exception
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user:schemas.User):
    if current_user.is_active == 'disabled':
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Separate function for token cleanup
def cleanup_expired_tokens(db: Session):
    old_tokens = db.query(models.Token).filter(models.Token.created_date < datetime.utcnow() - timedelta(days=1))
    old_tokens.delete()
    db.commit()

def get_sentiments_by_user(db: Session, user_id: int):
    return db.query(models.SentimentResult).filter(models.SentimentResult.user_id == user_id).all()


