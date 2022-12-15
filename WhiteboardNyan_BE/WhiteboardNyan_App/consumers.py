import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

class WhiteboardConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("Disconnected")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        response = json.loads(text_data)
        event = response.get("event", None)
        data = response.get("data", None)

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'send_message',
            'data': data,
            'event': event
        })

    def send_message(self, res):
        self.send(text_data=json.dumps({
            "type": "websocket.send",
            "payload": res,
        }))
