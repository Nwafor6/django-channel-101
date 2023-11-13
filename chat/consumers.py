import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

active_user=[]
class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print(self.channel_name, "Helooo")
        channel_name=self.channel_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        # Send a private welcome message to the connected user
        self.send(text_data=json.dumps({
            'message': 'Welcome to our website!'
        }))
        active_user.append(self)
        if len(active_user) > 1:
            active_user[0].send(text_data=json.dumps({
            'message': f'{self.channel_name} has just joined out wesite!'
        }))


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print( self.room_group_name, self.channel_name, "At disconnet")

    # Receive message from WebSocket
    def receive(self, text_data):
        print("Called 1")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        print("called 2")
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))