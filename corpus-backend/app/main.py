from fastapi import FastAPI

from app.db import Base, engine
from app.routers.stickies import router as stickies_router
from app.routers.tags import router as tags_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Create tables on startup (consider Alembic for production migrations)
    Base.metadata.create_all(bind=engine)

app.include_router(stickies_router)
app.include_router(tags_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Corpus API"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}