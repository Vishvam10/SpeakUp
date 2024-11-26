import warnings

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from globals.setter import set_mongodb_client

from api.tags import APITags
from api.router import MainRouter

warnings.filterwarnings("ignore")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Application starting")
        
        set_mongodb_client()

        yield
        
    except Exception as e:
        print(f"An error occurred during setup: {e}")
    finally:
        print("Application stopping")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(MainRouter, prefix="/v1")


@app.get("/", tags=[APITags.HEALTH_CHECK])
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
