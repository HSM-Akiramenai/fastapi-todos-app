from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app import schemas, database, models
from sqlalchemy.orm import Session
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

key, algorithm, minutes = settings.secret_key, settings.algorithm, settings.access_token_expire_minutes

SECRET_KEY = key
ALGORITHM = algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = minutes

def create_access_token(user_data: dict):
    payload = user_data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(access_token: str, credentials_exception):

    try: 
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = str(payload.get("user_id"))
        if not id:
            raise credentials_exception
        user_info = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return user_info
    
def get_current_user(user_access_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail=f"Could not validate credentials",
                                   headers={"WWW-Authenticate": "Bearer"})
    
    user_info = verify_access_token(user_access_token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == user_info.id).first()

    return user