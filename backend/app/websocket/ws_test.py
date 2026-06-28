from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        await websocket.send_text(f"Echo: {msg}")
