import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Subquery, OuterRef
from .models import ChatMessages, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_name = f"{self.sender_id}_{self.receiver_id}"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch old messages on page load
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'sender_id': message['sender_username']
            }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        msgReceiverId = text_data_json['msgReceiverId']
        receiver_id = self.receiver_id  # Extracted from the URL or context

        sender_username = await self.save_message(sender_id=sender_id, receiver_id=msgReceiverId, message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_username': sender_username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_username
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        # from .models import ChatMessages, User
        chat_obj = ChatMessages.objects.create(
            sender_id_id=sender_id,
            receiver_id_id=receiver_id,
            content=message,
        )
        chat_obj.save()
        return User.objects.get(id=sender_id).username


    @database_sync_to_async
    def get_messages(self):
        # from .models import ChatMessages, User
        username_subquery = User.objects.filter(id=OuterRef('sender_id')).values('username')[:1]
        message_list = list(
            ChatMessages.objects.filter(
                sender_id_id__in=[self.sender_id, self.receiver_id],
                receiver_id_id__in=[self.sender_id, self.receiver_id]
            )
            .order_by('timestamp')
            .annotate(sender_username=Subquery(username_subquery))
            .values('content', 'sender_username')
        )
        return message_list
