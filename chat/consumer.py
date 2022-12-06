import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import Account
from convos.models import Conversation, Message


@sync_to_async
def db_message(receiver, sender, message):
    receiver_ = Account.objects.get(username=receiver)
    sender_ = Account.objects.get(username=sender)
    convo = Conversation.get(user1=receiver_, user2=sender_)[0]
    message_obj = Message(conversation=convo, text=message, sender=sender_)
    message_obj.save()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await (self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json['receiver']

        # receiver_ = await Account.objects.get(username=receiver)
        # sender_ = await sync_to_async(Account.objects.get(username=sender))()
        # convo = await sync_to_async(Conversation.get(user1=receiver_, user2=sender_)[0])()
        # message_obj = await sync_to_async(Message(conversation=convo, text=message, sender=sender_))()
        # message_obj.save()
        # Send message to room group
        await db_message(receiver=receiver, sender=sender, message=message)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", 'sender': sender, 'receiver': receiver, "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event['sender']
        receiver = event['receiver']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'sender':sender, 'receiver':receiver, "message": message}))

    async def status_notifier(self, event):
        await self.send_json(event)