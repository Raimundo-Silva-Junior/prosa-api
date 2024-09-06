from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .utils.auth import AuthenticateWebsocket
import json
from rest_framework import status
from .utils.mensager import Mensager


class ChatConsumer(WebsocketConsumer):
    
    def connect(self) -> None:
        data = AuthenticateWebsocket(self.scope)
        if not data.valid:
            self.chatroom_name = None
            return self.close(reason="User not found", code=status.HTTP_401_UNAUTHORIZED)
        self.user, self.chat = data.user, data.chat
        self.chatroom_name = str(data.chat.id)
        self.chat.save()
        async_to_sync(self.channel_layer.group_add)(self.chatroom_name, self.channel_name)
        self.accept()

    def receive(self, text_data: str) -> None:
        messager = Mensager(chat=self.chat, user=self.user)
        messager.save(text_data)
        
    def send_message(self, event, type="send_message") -> None:
        message = event['text']
        self.send(
            text_data=json.dumps(
                {
                    'type': 'chat',
                    'id': str(self.chat.id),
                    "username": event['username'],
                    'message': message
                },
                ensure_ascii=False
            ) 
        )
        
    def disconnect(self, close_code: str) ->  None:
        if self.chatroom_name: 
            async_to_sync(self.channel_layer.group_discard)(self.chatroom_name, self.channel_name)
        self.close()
        
        