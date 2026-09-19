from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        previous = self.active_connections.get(user_id)
        if previous and previous is not websocket:
            await previous.close(code=1000)
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str, websocket: WebSocket | None = None):
        if websocket is None or self.active_connections.get(user_id) is websocket:
            if user_id not in self.active_connections:
                return
            del self.active_connections[user_id]

    def is_connected(self, user_id: str) -> bool:
        return user_id in self.active_connections

    async def send_to_user(self, user_id: str, data: dict) -> bool:
        websocket = self.active_connections.get(user_id)

        if websocket:
            try:
                await websocket.send_json(data)
                return True
            except (WebSocketDisconnect, RuntimeError):
                self.disconnect(user_id, websocket)

        return False