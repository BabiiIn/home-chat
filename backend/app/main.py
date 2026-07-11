from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router
from app.websocket.routes import router as websocket_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS (React будет работать на другом порту)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "HC backend is running"}

app.include_router(auth_router)
app.include_router(websocket_router)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
