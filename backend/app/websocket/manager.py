from typing import Dict, Set
from fastapi import WebSocket

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)

    async def disconnect(self, room: str, websocket: WebSocket):
        if room in self.rooms:
            self.rooms[room].discard(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: str):
        if room in self.rooms:
            for ws in list(self.rooms[room]):  # ← добавили list()
                try:
                    await ws.send_text(message)
                except Exception:
                    # WebSocket закрыт — удаляем его
                    self.rooms[room].discard(ws)   # ← добавили

            # Если комната пустая — удаляем
            if not self.rooms[room]:
                del self.rooms[room]               # ← добавили

