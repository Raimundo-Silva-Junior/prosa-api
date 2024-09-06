from django.db.models.signals import post_save
from .models import Message
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .utils.mensager import Mensager
import json
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Message) 
def message_handler(sender: Message, instance: object, created: bool, **kwargs):
    if created:
        chatroom_name = str(instance.chat.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            chatroom_name,
            {
                "type": "send_message",
                "text": instance.text,
                "username": instance.created_by.username
            },
        )
        messager = Mensager(user=instance.created_by, chat=instance.chat)
        messager.update(instance.id, status=Message.DELIVERED)
    