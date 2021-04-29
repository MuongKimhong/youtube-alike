import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from youtube.models import Notification


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, 
                                                        self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        json_data = json.loads(text_data)
        notification = Notification.objects.create(user_id=json_data['user_id'],
                                                   content=json_data['content'],
                                                   url=json_data['url'])
        notification_message = {
            'sender_name': json_data['sender_name'],
            'user_id': json_data['user_id'],
            'content': json_data['content'],
            'url'    : json_data['url']
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification_response',
                'message': notification_message
            }
        )

    # Receive message from room group
    def notification_response(self, event):
        notification_message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': notification_message}))
