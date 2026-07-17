import { useEffect, useState, useRef } from "react";
import WebSocketClient from "../services/WebSocketClient";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  const token = localStorage.getItem("token");
  const room = "family";
  const wsRef = useRef(null);

  useEffect(() => {
    if (!token) {
      console.log("No token found, skipping WebSocket connection");
      return;
    }

    const ws = new WebSocketClient(
      `ws://localhost:8000/ws/chat?room=${room}&token=${token}`,
    );
    ws.connect();
    wsRef.current = ws;

    ws.onOpen(() => {
      setMessages([]); // очищаем историю перед загрузкой новой
    });

    ws.onMessage((msg) => {
      console.log("WS message:", msg); 
      setMessages((prev) => [...prev, msg]);
    });

    return () => {
      console.log("Closing WS from Chat page");
      if (ws.ws) {
        ws.shouldReconnect = false;
        ws.ws.close();
      }
    };
  }, [token]);

  function sendMessage() {
    if (!wsRef.current) return;

    wsRef.current.sendMessage({
      type: "text",
      content: text,
    });
    setText("");
  }

  function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file || !wsRef.current) return;

    const reader = new FileReader();

    reader.onload = () => {
      const base64 = reader.result.split(",")[1];

      wsRef.current.sendMessage({
        type: "image",
        filename: file.name,
        data: base64,
      });
    };

    reader.readAsDataURL(file);
  }

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto" }}>
      <h1>Chat</h1>

      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "300px",
          overflowY: "auto",
          marginBottom: "20px",
        }}
      >
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: "8px" }}>
            {m.type === "text" && <div>{m.content}</div>}
            {m.type === "image" && (
              <img src={`http://localhost:8000${m.url}`} alt="image" style={{ maxWidth: "200px", borderRadius: "8px" }} />
            )}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "10px" }}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type message..."
          style={{ flex: 1, padding: "10px" }}
        />
        <input type="file" accept="image/*" onChange={handleImageUpload} />

        <button
          onClick={sendMessage}
          style={{
            padding: "10px 20px",
            background: "#333",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
