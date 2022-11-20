import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class WhiteboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(text_data)
        response = json.loads(text_data)
        event = response.get("event", None)
        data = response.get("data", None)

        if event == "JOIN":
            pass
        else:
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'data': data,
                'event': event
            })

    async def send_message(self, res):
        print("RES: " + json.dumps(res))
        await self.send(text_data=json.dumps({
            "type": "websocket.send",
            "payload": res,
        }))
#        await self.send(text_data=json.dumps({
#            "payload": res,
#        }))
