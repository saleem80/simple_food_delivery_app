import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage
from bookings.models import Booking

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = f'chat_{self.booking_id}'
        
        # Check if user has permission to access this chat
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        
        booking = await self.get_booking(self.booking_id)
        if not booking:
            await self.close()
            return
        
        # Check permissions
        if not await self.has_chat_permission(user, booking):
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        user = self.scope["user"]
        
        # Save message to database
        chat_message = await self.save_message(user, self.booking_id, message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.mobile_number,
                'sender_type': user.user_type,
                'timestamp': chat_message.timestamp.isoformat(),
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_type = event['sender_type']
        timestamp = event['timestamp']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_type': sender_type,
            'timestamp': timestamp,
        }))
    
    @database_sync_to_async
    def get_booking(self, booking_id):
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None
    
    @database_sync_to_async
    def has_chat_permission(self, user, booking):
        # Only customer and assigned delivery partner can chat
        if booking.status != 'assigned' and booking.status not in ['started', 'reached', 'collected']:
            return False
        
        return (user == booking.customer or user == booking.delivery_partner)
    
    @database_sync_to_async
    def save_message(self, user, booking_id, message):
        booking = Booking.objects.get(id=booking_id)
        return ChatMessage.objects.create(
            booking=booking,
            sender=user,
            message=message
        )