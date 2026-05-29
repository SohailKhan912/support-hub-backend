from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.database import Base
from app.api.tickets import router as tickets_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support CRM API")
# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://192.168.0.123:8081",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include tickets router
app.include_router(tickets_router)


@app.get("/")
async def root():
    return {"message": "Support CRM API is running!", "docs": "/docs"}
