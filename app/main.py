from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.interview import router as interview_router
from app.api.websocket import router as websocket_router
from app.registry.competency_registry import competency_registry


@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        f"Loaded "
        f"{len(competency_registry.all())} "
        f"competencies."
    )

    yield


app = FastAPI(
    title="Interview AI Backend",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"],
)

app.include_router(
    websocket_router,
    prefix="/ws",
    tags=["WebSocket"],
)


@app.get("/")
def root():

    return {
        "status": "running"
    }