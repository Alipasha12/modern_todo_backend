from pydantic import BaseModel

class UserCreate(BaseModel):
    title: str
    
    
class UserUpdate(BaseModel):
    title: str