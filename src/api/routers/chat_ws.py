from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from repositories import MessageRepository
from services import ChatParticipantService, AuthService

from dependencies import (
    get_message_repo,
    get_chat_participant_service,
    get_auth_service
)


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[int, list[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()

        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []

        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.active_connections:
            if websocket in self.active_connections[chat_id]:
                self.active_connections[chat_id].remove(websocket)

            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: dict):
        for connection in self.active_connections.get(chat_id, []):
            await connection.send_json(message)


manager = ConnectionManager()
router = APIRouter(
    prefix="/ws/chat",
    tags=["websocket_chat"]
)


@router.websocket("/{chat_id}")
async def chat_ws(
    websocket: WebSocket,
    chat_id: int,
    participant_service: ChatParticipantService = Depends(get_chat_participant_service),
    message_repo: MessageRepository = Depends(get_message_repo),
    auth_service: AuthService = Depends(get_auth_service),
):
    # 🔐 Авторизация
    token = websocket.query_params.get("token")
    print("Token:", token)
    payload = auth_service.verify_token(token)
    print("Payload:", payload)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=1008)
        return

    user = await auth_service.user_repo.get_data_by_id(payload["user_id"])

    if not user:
        await websocket.close(code=1008)
        return

    await participant_service.verify_user_in_chat(chat_id, user.id)
    try:
        await participant_service.verify_user_in_chat(chat_id, user.id)
    except HTTPException as e:
        await websocket.close(code=1008)
        return
    await manager.connect(chat_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            message = await message_repo.create_data({
                "chat_id": chat_id,
                "sender_id": user.id,
                "content": content
            })

            response = {
                "id": message.id,
                "chat_id": chat_id,
                "sender_id": user.id,
                "content": content,
                "created_at": str(message.created_at)
            }

            await manager.broadcast(chat_id, response)

    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
