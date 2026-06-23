from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import router as auth_router

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to HC WebSocket")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")

app.include_router(auth_router)
