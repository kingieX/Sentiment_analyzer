from fastapi import Depends, FastAPI, HTTPException,status,Query
from fastapi.responses import JSONResponse,Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from datetime import datetime
import crud,schemas,models
import database 
from typing import List
from typing import Any
import config
import utils
import jwt
from uuid import uuid4
import logging

models.database.Base.metadata.create_all(bind=database.engine)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

jwtb = utils.JWTBearer()
# In-memory cache for user data
user_cache = {}

app = FastAPI()
origins = [
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/info")
async def info() -> dict[str, str]:
    return {
        "app_name": config.settings.app_name,
        "admin_email": config.settings.admin_email,
    }

@app.post("/signup")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> JSONResponse:
     hashed_password = utils.get_hashed_password(user.password)
     existing_user = db.query(models.User).filter_by(email=user.email).first()
     existing_username = db.query(models.User).filter_by(username=user.username).first()
     if existing_user:
        error_message = {"error": "Email already exists"}
        return JSONResponse(content=error_message, status_code=status.HTTP_404_NOT_FOUND)
     if existing_username:
         error_message = {"error":"Username already exist"}
         return JSONResponse(content=error_message, status_code=status.HTTP_404_NOT_FOUND)
     try:
         new_user = models.User(username=user.username,fullname=user.fullname, email=user.email, password=hashed_password)
         db.add(new_user)
         db.commit()
         db.refresh(new_user)
         # Convert datetime objects to strings
         created_at_str = new_user.createdAt.strftime("%Y-%m-%dT%H:%M:%SZ")
         updated_at_str = new_user.updatedAt.strftime("%Y-%m-%dT%H:%M:%SZ")

         user_dict = {
             "id": new_user.id,
             "username": new_user.username,
             "email": new_user.email,
             "is_active": new_user.is_active,
             "createdAt": created_at_str,
             "updatedAt": updated_at_str,
            }
     
         return JSONResponse(content=user_dict, status_code=status.HTTP_201_CREATED)
     except IntegrityError as e:
         logger.error(f"IntegrityError: {e}")
         db.rollback()
         error_message = {"error": "Username already exists"}
         return JSONResponse(content=error_message, status_code=status.HTTP_400_BAD_REQUEST)



@app.post("/login", summary="Create access and refresh tokens for user", response_model=schemas.Token)
async def login(request: schemas.UserIn, db: Session = Depends(get_db)) -> dict[str, str]:
    # Log the login attempt
    logger.info(f"Login attempt from email: {request.email}")

    try:
        user = crud.get_user_by_email(db, email=request.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        if not utils.verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        
        # Generate access and refresh tokens
        access_token = utils.create_access_token(subject=user.id)
        refresh_token = utils.create_refresh_token(subject=user.id)
        # Create and save token data
        token_db = models.Token(user_id=user.id, access_token=access_token, refresh_token=refresh_token, status=True)
        db.add(token_db)
        db.commit()
        db.refresh(token_db)
        # Log successful login
        logger.info(f"Login successful for user: {user.email}")

        return {"user_id": user.id, "access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        logger.error(f"Login failed for email: {request.email}: {e}")
        raise e

@app.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not utils.validate_password(request.new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password does not meet minimum requirements")

    if not utils.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    try:
        user.password = utils.get_hashed_password(request.new_password)
        db.commit()
        # Log successful password change
        logger.info(f"User: {user.email} successfully changed their password")
        return {"message": "Password changed successfully"}
    except Exception as e:
        # Log the error
        logger.error(f"Error changing password for user: {user.email}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error changing password")

@app.post("/logout")
async def logout(token: str = Depends(crud.oauth2_scheme), db: Session = Depends(get_db)):
    logging.info("Logout attempt")

    try:
        payload = jwt.decode(token, utils.JWT_SECRET_KEY, utils.ALGORITHM)
        user_id = payload["sub"]

        # Deactivate the user's access token
        existing_token = db.query(models.Token).filter(
            models.Token.user_id == user_id, models.Token.access_token == token
        ).first()
        if existing_token:
            existing_token.status = False
            db.add(existing_token)
            db.commit()
            db.refresh(existing_token)

        # Cleanup expired tokens (optional)
        crud.cleanup_expired_tokens(db)

        return {"message": "Logout successful"}

    except jwt.exceptions.InvalidTokenError:
        logging.error("Invalid token provided")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except Exception as e:
        logging.error(f"Logout failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="id", allowed=["id", "email", "created_at"]),
    sort_order: str = Query(default="asc", allowed=["asc", "desc"]),
    filter_by: str = Query(default=None),
):
    offset = (page - 1) * per_page
    cache_key = f"users_page_{page}_per_page_{per_page}"
    cached_users = user_cache.get(cache_key)

    if not cached_users:
        query = db.query(models.User)

        if filter_by:
            try:
                filter_by_field, filter_value = filter_by.split(":")
                query = query.filter(getattr(models.User, filter_by_field) == filter_value)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid filter format.")
        order_by_clause = text(f"{sort_by} {sort_order}")
        query = query.order_by(order_by_clause)
        users = query.limit(per_page).offset(offset).all()
        user_cache[cache_key] = users

    # Return cached or retrieved users
    return users


@app.get("/users/{user_id}", response_model= schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.post("/textinput", status_code=status.HTTP_201_CREATED)
def create_text(text_input: schemas.TextInputCreate, db: Session = Depends(get_db)):
    try:
        new_text_input = models.TextInput(**text_input.dict())
        db.add(new_text_input)
        db.commit()
        db.refresh(new_text_input)
        return new_text_input
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/textinputs")
def read_textinputs(db: Session = Depends(get_db)):
    all_textinputs = db.query(models.TextInput).all()
    return all_textinputs

@app.get("/textinput/{id}",status_code=200)
def get(id:int,db:Session=Depends(get_db)):
    db_text = db.query(models.TextInput).filter(models.TextInput.id == id).first()
    if db_text == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"social media text with such {id} does not exist")
    return db_text

@app.delete("/textinput/delete/{id}",status_code=204)
def delete_textinputs(id:int,db:Session=Depends(get_db)):
    delete_textinput = db.query(models.TextInput).filter(models.TextInput.id == id).first()
    if delete_textinput == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"social media text with such {id} does not exist")
    else:
        db.query(models.TextInput).filter_by(id=id).delete()
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/textinput/{id}")
def textinput_update(id: int, textinput: schemas.TextInputBase, db: Session = Depends(get_db)):
    updated_textinput = db.query(models.TextInput).filter(models.TextInput.id == id).first()

    if updated_textinput is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"social media text with ID {id} not found")

    # Update the attributes of the existing course
    for key, value in textinput.dict().items():
        setattr(updated_textinput, key, value)

    db.commit()
    db.refresh(updated_textinput)

    return updated_textinput


@app.post("/preferences", status_code=status.HTTP_201_CREATED)
def create_preference(preference: schemas.PreferenceSettingCreate, db: Session = Depends(get_db)):
    try:
        new_preference = models.PreferenceSetting(**preference.dict())
        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)
        return new_preference
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/preferences/{id}", status_code=200)
def get_preference(id: int, db: Session = Depends(get_db)):
    db_preference = db.query(models.PreferenceSetting).filter(models.PreferenceSetting.id == id).first()
    if db_preference is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PreferenceSetting with ID {id} not found")
    return db_preference

@app.delete("/preferences/delete/{id}", status_code=204)
def delete_preference(id: int, db: Session = Depends(get_db)):
    delete_preference = db.query(models.PreferenceSetting).filter(models.PreferenceSetting.id == id).first()
    if delete_preference is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PreferenceSetting with ID {id} not found")
    else:
        db.query(models.PreferenceSetting).filter_by(id=id).delete()
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/preferences/{id}")
def update_preference(id: int, preference: schemas.PreferenceSettingBase, db: Session = Depends(get_db)):
    updated_preference = db.query(models.PreferenceSetting).filter(models.PreferenceSetting.id == id).first()

    if updated_preference is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PreferenceSetting with ID {id} not found")

    # Update the attributes of the existing preference
    for key, value in preference.dict().items():
        setattr(updated_preference, key, value)

    db.commit()
    db.refresh(updated_preference)

    return updated_preference


@app.post("/sentiment", status_code=status.HTTP_201_CREATED)
def create_sentiment_result(sentiment_result: schemas.SentimentResultCreate,db: Session = Depends(get_db)):
    try:
        new_sentiment = models.SentimentResult(**sentiment_result.dict())

        # Add the new SentimentResult to the database
        db.add(new_sentiment)
        db.commit()
        db.refresh(new_sentiment)

        return new_sentiment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/sentiment/user/{user_id}", response_model=List[schemas.SentimentResult])
def get_sentiments_by_user(user_id: int, db: Session = Depends(get_db)):
    sentiments = crud.get_sentiments_by_user(db, user_id)
    if not sentiments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sentiments for User with ID {user_id} not found",
        )
    return sentiments

@app.delete("/sentiment/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sentiment_result(id: int, db: Session = Depends(get_db)):
    delete_sentiment_result = db.query(models.SentimentResult).filter(models.SentimentResult.id == id).first()
    if delete_sentiment_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SentimentResult with ID {id} not found")
    else:
        db.query(models.SentimentResult).filter_by(id=id).delete()
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

