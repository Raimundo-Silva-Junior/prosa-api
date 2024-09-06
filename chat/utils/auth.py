from typing import Any
from django.contrib.auth.models import User
from ..models import Chat
from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import Tuple
from dataclasses import dataclass



class AuthenticateWebsocket:
    """
    Authenticate websocket user
    return :
        AuthData(bool|User|Chat)
    """
    
    @dataclass
    class AuthData:
        valid: bool
        user: User | None
        chat: Chat | None

    def __new__(cls, scope: dict) -> AuthData:
        cls.scope = scope
        user = cls.__authenticate_websocket_user(cls)
        if not user:
            return cls.AuthData(False, user, None)
        chat = cls.__find_chat(cls, user)
        if not chat:
            return cls.AuthData(False, user, None)
        return cls.AuthData(True, user, chat)
    
    def __authenticate_websocket_user(self) -> User|None:
        for key, value in self.scope["headers"]:
            if key == b'authorization':
                value = value.decode()
                if "Bearer" in value:
                    token =  value.replace("Bearer ", "")
                    break
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(token)
        except Exception:
            ...
        return auth.get_user(validated_token)

    def __find_chat(self, user: User) -> Chat|None:
        chat_id = self.scope.get("query_string")
        if chat_id:
            if chat_id.decode().startswith("id="):
                chat_id = chat_id.decode().replace("id=", "")
        chat = user.chats.filter(id=chat_id)
        if chat:
            return chat.first()
        
        

