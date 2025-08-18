from fastapi import FastAPI
from app.routers.stickies import router as stickies_router
from app.routers.tags import router as tags_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Corpus API"}

app.include_router(stickies_router)
app.include_router(tags_router)