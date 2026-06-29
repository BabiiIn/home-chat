import asyncio
import websockets
import json
import os
from dotenv import load_dotenv


async def test():


    load_dotenv()    
    token = os.getenv("TEST_TOKEN")
    uri = f"ws://localhost:8000/ws/chat?room=family&token={token}"

    async with websockets.connect(uri) as ws:
        # читаем историю сообщений
        await ws.recv()

        # отправляем русское сообщение
        await ws.send(json.dumps({
            "type": "text",
            "content": "УРА! Привет!"
        }))

        # получаем ответ на наше сообщение
        response = await ws.recv()
        print("Сырой JSON:", response)
        print("Декодированный текст:", json.loads(response)["content"])
        print(json.dumps(json.loads(response), ensure_ascii=False))


asyncio.run(test())
