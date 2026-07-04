import json
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.auth.jwt_utils import verify_token
from app.websocket.manager import RoomManager
from app.database import SessionLocal
from app.services.messages import save_message, get_last_messages
from app.services.files import save_image


router = APIRouter(prefix="/ws")
manager = RoomManager()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
#   ПРОСТОЙ ЭХО-ЭНДПОИНТ
# ---------------------------------------------------------
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
            text = await websocket.receive_text()
            await websocket.send_text(f"{user['email']}: {text}")
    except WebSocketDisconnect:
        print("Client disconnected")


# ---------------------------------------------------------
#   ОСНОВНОЙ ЧАТ
# ---------------------------------------------------------
@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    token = websocket.query_params.get("token")
    room = websocket.query_params.get("room")

    if not token or not room:
        await websocket.close(code=1008)
        return

    try:
        user = verify_token(token)
    except:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    await manager.connect(room, websocket)

    # -----------------------------------------------------
    #   ОТПРАВКА ИСТОРИИ
    # -----------------------------------------------------
    history = get_last_messages(db, room)

    for msg in reversed(history):

        # текст
        if msg.message_type == "text" and msg.content:
            await websocket.send_text(json.dumps({
                "type": "text",
                "user_id": msg.user_id,
                "content": msg.content
            }))

        # картинка
        elif msg.message_type == "image" and msg.file_path:
            await websocket.send_text(json.dumps({
                "type": "image",
                "user_id": msg.user_id,
                "url": msg.file_path
            }))

        # битые записи пропускаем
        else:
            continue

    # -----------------------------------------------------
    #   ОСНОВНОЙ ЦИКЛ ПРИЁМА СООБЩЕНИЙ
    # -----------------------------------------------------
    try:
        while True:

            ws_msg = await websocket.receive()

            # текстовый JSON
            if ws_msg["type"] == "websocket.receive" and ws_msg.get("text"):
                data = json.loads(ws_msg["text"])

            # бинарный JSON (большие base64)
            elif ws_msg["type"] == "websocket.receive" and ws_msg.get("bytes"):
                data = json.loads(ws_msg["bytes"].decode("utf-8"))

            else:
                continue

            # -------------------------------------------------
            #   ТЕКСТОВОЕ СООБЩЕНИЕ
            # -------------------------------------------------
            if data["type"] == "text":
                content = data["content"]

                save_message(
                    db,
                    int(user["sub"]),
                    room,
                    content=content,
                    message_type="text",
                    file_path=None
                )

                await manager.broadcast(room, json.dumps({
                    "type": "text",
                    "user_id": user["sub"],
                    "content": content
                }))

            # -------------------------------------------------
            #   ИЗОБРАЖЕНИЕ
            # -------------------------------------------------
            elif data["type"] == "image":
                file_url = save_image(room, data["filename"], data["data"])

                save_message(
                    db,
                    int(user["sub"]),
                    room,
                    content=None,
                    message_type="image",
                    file_path=file_url
                )

                await manager.broadcast(room, json.dumps({
                    "type": "image",
                    "user_id": user["sub"],
                    "url": file_url
                }))

    except WebSocketDisconnect:
        await manager.disconnect(room, websocket)

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        await manager.disconnect(room, websocket)

    
    
