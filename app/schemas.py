from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str

class CustomerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    city: Optional[str] = None
    
    class Config:
        from_attributes = True
