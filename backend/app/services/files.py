import os
import base64
from datetime import datetime

UPLOAD_DIR = "app/uploads"

def save_image(room: str, filename: str, base64_data: str) -> str:
    room_path = os.path.join(UPLOAD_DIR, room)
    os.makedirs(room_path, exist_ok=True)

    # уникальное имя файла
    timestamp = int(datetime.utcnow().timestamp())
    safe_name = f"{timestamp}_{filename}"

    file_path = os.path.join(room_path, safe_name)

    # декодируем base64
    file_bytes = base64.b64decode(base64_data)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # путь, который будет доступен через HTTP
    return f"/uploads/{room}/{safe_name}"
