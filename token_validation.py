from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
import secrets


# SECRET_KEY = secrets.token_urlsafe(32)
SECRET_KEY = "vYwteHF2olSECLvniVb-XeBbgwXuhOT4fwhItyjORfo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    print(data, "details of login user")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    print(SECRET_KEY, "secret key for login")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)