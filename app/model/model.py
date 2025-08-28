from app.database.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime
class Todo(Base):
    __tablename__="todo"
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )