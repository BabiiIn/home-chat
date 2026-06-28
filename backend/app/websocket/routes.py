from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.auth.jwt_utils import verify_token

router = APIRouter(prefix="/ws")

@router.websocket("/echo")
async def websocket_echo(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        user = verify_token(token)
    except:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"{user['email']}: {message}")
    except WebSocketDisconnect:
        print("Client disconnected")
