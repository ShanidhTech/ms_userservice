from http.client import HTTPException
from fastapi import FastAPI, Depends, HTTPException, status

from database import get_db
from models import User, UserType
from schemas import UserCreate, UserLogin, UserResponse, UserTypeCreate, UserTypeResponse
from token_validation import create_access_token, hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()

users = []

# @app.post("/users/")
# def create_user(user: dict):
#     users.append(user)
#     return {"message": "User registered successfully", "user": user}

@app.post("/register/user", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.email == user.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@app.post("/login/")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"email": db_user.email, "id": db_user.id, "user_type": db_user.user_type, "username": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/usertype/create", response_model=UserTypeResponse)
async def create_user_type(user_type: UserTypeCreate, db: AsyncSession = Depends(get_db)):
    existing_type = await db.execute(select(UserType).where(UserType.user_type == user_type.user_type))
    if existing_type.scalar():
        raise HTTPException(status_code=400, detail="User type already exists")

    new_type = UserType(user_type=user_type.user_type)
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)

    return new_type

@app.get("/users/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
