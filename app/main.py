from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService
from app.database.database import engine, Base, get_db
from app.model.model import Todo
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:

        table_exists = await conn.run_sync(
            lambda sync_conn: engine.dialect.has_table(sync_conn, Todo.__tablename__)
        )
        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(debug=True, lifespan=lifespan)

origins = ["http://localhost:5173", "https://zaif-todos.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome():
    return "hello"


@app.post("/create")
async def createtodo(user_input: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    result = await user_service.create_todo(user_input)
    return result


@app.post("/update")
async def updatetodo(
    user_id: int, user_input: UserUpdate, db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    result = await user_service.update_todo(user_input, user_id)
    return result


@app.get("/todos")
async def get_todos(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    result = await user_service.get_all_todos()
    return result


@app.delete("/delete")
async def deletetodo(user_id: int, db: AsyncSession = Depends(get_db)):
    user_db = await db.get(Todo, user_id)
    if user_db:
        await db.delete(user_db)
        await db.commit()
        return "deleted succesfully"
    return "not found any todo on this id"
