from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate,UserUpdate
from app.model.model import Todo
from typing import List
from sqlalchemy import select
class UserService:
    def __init__(self, db:AsyncSession):
        self.db: AsyncSession = db
    
    async def get_todo_by_id(self,user_id:int) -> Todo:
        result = await self.db.get(Todo,user_id)
        return result
    
    async def get_all_todos(self)->List[Todo]:
        stmt = select(Todo)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def create_todo(self,user_input:UserCreate):
        user_model = Todo(**user_input.model_dump())
        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)
        return user_model
    
    async def update_todo(self, user_input: UserUpdate, user_id: int):
        user_in_db = await self.get_todo_by_id(user_id)
        if not user_in_db:
            return {"error":"user id se not found"}
        update_data = user_input.model_dump(exclude_unset=True)
        for key,value in update_data.items():
            setattr(user_in_db, key, value)
        await self.db.commit()
        await self.db.refresh(user_in_db)
        return user_in_db
