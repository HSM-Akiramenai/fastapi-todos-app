from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

db_usrname, db_pwd, db_hostname, db_port, db_name = settings.database_username, settings.database_password, settings.database_hostname, settings.database_port, settings.database_name

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_usrname}:{db_pwd}@{db_hostname}:{db_port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()