import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.apps import apps


@sync_to_async
def db_message(receiver, sender, message):

    account_model = apps.get_model('accounts.Account')
    conversation_model = apps.get_model('convos.Conversation')
    message_model = apps.get_model('convos.Message')

    sender_ = account_model.objects.get(username=sender)
    convo = conversation_model.get_by_pk(pk=receiver)

    message_obj = message_model(conversation=convo, text=message, sender=sender_)
    message_obj.save()


class ChatConsumer(AsyncWebsocketConsumer):
    def _get_connection_id(self):
        return ' '.join(e for e in self.channel_name if e.isalnum())

    async def connect(self):
        scope = self.scope
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

        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json['receiver']

        await db_message(receiver=receiver, sender=sender, message=message)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", 'sender': sender, 'receiver': receiver, "message": message}
        )

    async def forward_group_message(self, event):
        await self.send(json.dumps(event['data'], default=str))

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event['sender']
        receiver = event['receiver']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'sender':sender, 'receiver':receiver, "message": message}))


