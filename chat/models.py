from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Chat(models.Model):
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    members = models.ManyToManyField(User, related_name="chats")
    
    @property
    def count(self):
        return self.members.count()
    
class Message(models.Model):
    
    SENT, SERVER, DELIVERED = 0, 1, 2
    
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=SENT, choices=((SENT, 0), (SERVER, 1), (DELIVERED, 2)))
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"id: {self.id}, created_by: {self.created_by.username}"



        