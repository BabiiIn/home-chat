import asyncio
import websockets
import json
import base64
import os
from dotenv import load_dotenv

async def test():
    
    load_dotenv()
    token = os.getenv("TEST_TOKEN")
    uri = f"ws://localhost:8000/ws/chat?room=family&token={token}"

    # путь к файлу рядом со скриптом
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "test.jpg")

    print("Используем файл:", image_path)

    with open(image_path, "rb") as f:
        file_bytes = f.read()

    print("Размер файла:", len(file_bytes), "байт")

    encoded = base64.b64encode(file_bytes).decode("utf-8")

    async with websockets.connect(uri) as ws:

        # ---------- ЧИТАЕМ ИСТОРИЮ ----------
        print("Читаем историю...")
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.2)
                print("История:", msg)

            # если сообщение НЕ текст и НЕ картинка — значит история закончилась
            # if '"type": "text"' not in msg and '"type": "image"' not in msg:
            except asyncio.TimeoutError:
                print("История закончилась.")
                break

        # ---------- ОТПРАВЛЯЕМ КАРТИНКУ ----------
        payload = {
            "type": "image",
            "filename": "test.jpg",
            "data": encoded
        }
        
        # print("Отправляем JSON:", payload)
        await ws.send(json.dumps(payload))

        # ---------- ЧИТАЕМ ОТВЕТ НА КАРТИНКУ ----------
        response = await ws.recv()
        print("Ответ сервера:", response)

asyncio.run(test())
