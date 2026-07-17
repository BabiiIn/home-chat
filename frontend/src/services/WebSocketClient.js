export default class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectDelay = 1000;
    this.messageHandlers = [];
    this.closeHandlers = [];
    this.openHandlers = [];
    this.shouldReconnect = true;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("WebSocket connected:", this.url);
      this.openHandlers.forEach((cb) => cb());
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messageHandlers.forEach((cb) => cb(data));
    };

    this.ws.onclose = () => {
      console.log("WebSocket closed, reconnecting...");
      this.closeHandlers.forEach((cb) => cb());
    
      if (this.shouldReconnect) {
        setTimeout(() => this.reconnect(), this.reconnectDelay);
      }
    };

    this.ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      this.ws.close();
    };
  }

  reconnect() {
    console.log("Reconnecting WebSocket...");
    this.connect();
  }

  sendMessage(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn("WebSocket is not open. Cannot send message.");
    }
  }

  onOpen(callback) {
    this.openHandlers.push(callback);
  }

  onMessage(callback) {
    this.messageHandlers.push(callback);
  }

  onClose(callback) {
    this.closeHandlers.push(callback);
  }
}
