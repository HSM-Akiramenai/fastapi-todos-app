from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.database import Base, get_db
from app.main import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
import pytest


db_usrname, db_pwd, db_hostname, db_port, db_name = settings.database_username, settings.database_password, settings.database_hostname, settings.database_port, settings.database_name

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_usrname}:{db_pwd}@{db_hostname}:{db_port}/{db_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)