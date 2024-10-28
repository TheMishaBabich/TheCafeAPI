import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.routers import auth_router
from db import Base, engine

app = FastAPI(
    title="CafeAPI",
    description="Pet-project, created for business",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

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
