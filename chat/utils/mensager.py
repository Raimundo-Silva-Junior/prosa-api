from django.contrib.auth.models import User
from ..models import Chat, Message
from dataclasses import dataclass

@dataclass
class Mensager:
    user: User
    chat: Chat
        
    def save(self, text: str):
        Message.objects.create(
            chat=self.chat,
            created_by=self.user,
            status=Message.SERVER,
            text=text
        )
    def delete(self, id: int):
        Message.objects.filter(id=id).delete()
        
    def update(self, id: int, status: str):
        
        Message.objects.filter(id=id).update(status=status)