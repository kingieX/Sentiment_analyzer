from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import List

class Token(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    

class TokenData(BaseModel):
    user_id: str
    access_token:str
    refresh_token:str
    status: bool
    created_date: datetime


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    fullname: str | None = None
    is_active: bool | None = None

class User(UserOut):
    password: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password:str
    fullname:str | None = None
    is_active: bool | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class changepassword(BaseModel):
    email: EmailStr
    old_password:str
    new_password:str
    

class TextInputBase(BaseModel):
    text_content: str
    text_title: str
    language: str

class TextInputCreate(TextInputBase):
    pass

class TextInput(TextInputBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class SentimentResultBase(BaseModel):
    label:str
    score: float

class SentimentResultCreate(SentimentResultBase):
    pass

class SentimentResult(SentimentResultBase):
    id: int
    label:str
    created_at: datetime
    user_id: int
    text_id: int

    class Config:
        from_attributes = True

class PreferenceSettingBase(BaseModel):
    theme: str
    notification: bool
    language_preference: str

class PreferenceSettingCreate(PreferenceSettingBase):
    pass

class PreferenceSetting(PreferenceSettingBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True





    
