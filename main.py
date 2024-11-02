import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.routers import auth_router
from db import Base, engine
from menu.routers import menu_router

app = FastAPI(
    title="CafeAPI",
    description="Pet-project, created for cafe business",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])

origins = [
    "http://127.0.0.1:3157",
    "http://localhost:3157",
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
