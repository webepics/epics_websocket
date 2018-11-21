#!/usr/bin/env python
"""
Websocket server
"""

import json
import asyncio
import websockets


class Message:
    """
    pass
    """

    def __init__(self, message_type, message_data=None, message_global=False):
        self._type = message_type
        self._data = message_data
        self._global = message_global
        self._binary = isinstance(message_data, bytes)

    @classmethod
    def from_json(cls, message):
        message = json.loads(message)

        is_global = message['global'] if 'global' in message.keys() else False

        try:
            return Message(message['type'], message['data'], message_global=is_global)
        except KeyError:
            return Message(message['type'], message_global=is_global)

    @property
    def json(self):
        return json.dumps({'type': self._type, 'data': self._data})

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def is_global(self):
        return self._global

    @property
    def is_binary(self):
        return self._binary


class WebsocketServer:
    """
    Pass
    """

    def __init__(self, port=None, debug=False):

        self.port = port if port is not None else 6064
        self._debug = debug
        self._connected = set()

        self.recv_queue = asyncio.Queue()
        self.send_queue = asyncio.Queue()
        self.reply_task = asyncio.ensure_future(self.reply_consumer())
        self.recv_task = asyncio.ensure_future(self.recv_consumer())

    async def handler(self, websocket, path):
        """
        Pass
        """
        self._connected.add(websocket)

        while True:
            listener_task = asyncio.ensure_future(websocket.recv())
            await asyncio.wait([listener_task])
            try:
                message = listener_task.result()
            except websockets.ConnectionClosed:
                listener_task.cancel()
                self._connected.remove(websocket)
                return
            await self.recv_queue.put({'websocket': websocket, 'message': message})

    async def recv_consumer(self):
        """
        Pass
        """
        while True:
            recv = await self.recv_queue.get()
            message = Message.from_json(recv['message'])
            websocket = recv['websocket']

            if message.type[0] == '_':
                return
            method = getattr(self, message.type)
            if method.__qualname__.split('.')[0] == self.__class__.__name__:
                if message.data is not None:
                    task = asyncio.ensure_future(method(**message.data))
                else:
                    task = asyncio.ensure_future(method())

                def callback(future):
                    reply = future.result()
                    if reply is not None:
                        self.send_queue.put_nowait({'websocket': websocket,
                                                    'message': reply})

                task.add_done_callback(callback)

    async def reply_consumer(self):
        """
        Pass
        """
        while True:
            reply = await self.send_queue.get()
            message = reply['message']
            websocket = reply['websocket']

            if message.is_binary:
                if message.is_global:
                    _ = [await ws.send(message.data) for ws in self._connected]
                else:
                    await websocket.send(message.data)
            else:
                if message.is_global:
                    _ = [await ws.send(message.json) for ws in self._connected]
                else:
                    await websocket.send(message.json)

    def run(self):
        """
        Pass
        """
        start_server = websockets.serve(self.handler, '0.0.0.0', self.port)
        asyncio.get_event_loop().set_debug(self._debug)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
