from fastapi import FastAPI, Request, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi.middleware.cors import CORSMiddleware

# Create tables in the database
# models.Base.metadata.create_all(bind=engine)

# Create a logging directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/myapp.log', maxBytes=10000000, backupCount=10),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Create FastAPI instance
app = FastAPI()  

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the error details for debugging purposes
    logger.error(f"Unexpected error occurred: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# Path Operation for the root endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}


