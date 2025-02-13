from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserTypeCreate(BaseModel):
    user_type: str

class UserTypeResponse(UserTypeCreate):
    id: int
    user_type: str

    class Config:
        from_attributes = True        
