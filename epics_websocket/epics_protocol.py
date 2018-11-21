import asyncio
from epics_websocket.webwebsocket_server import WebsocketServer, Message
from caproto.threading.client import Context
from functools import partial


class EpicsServerProtocol(WebsocketServer):
    """ Scatterbrain websocket protocol. """

    def __init__(self, port=6064, debug=False):
        super().__init__(port, debug=debug)
        self.ctx = Context()
        self.pvs = {}
        # self.sub_map = {}
        self.loop = asyncio.get_event_loop()

    async def subscribe_pv(self, pv_name):
        try:
            self.pvs[pv_name]['count'] += 1
        except KeyError:
            pv_obj, = self.ctx.get_pvs(pv_name)
            sub = pv_obj.subscribe()
            self.pvs[pv_name] = {
                'pv_obj': pv_obj,
                'sub': sub,
                'count': 0,
                'callback': partial(self.callback, pv_name)
            }
            sub.add_callback(self.pvs[pv_name]['callback'])
        return Message('Subscribe', 'Success')

    async def unsubscribe_pv(self, pv):
        try:
            self.pvs[pv]['count'] -= 1
            if self.pvs[pv]['count'] <= 0:
                del self.pvs[pv]
        except KeyError:
            pass

    async def put_pv(self, pv_name, value):
        self.pvs[pv_name]['pv_obj'].write(value)

    def callback(self, pv_name, response):
        self.loop.call_soon_threadsafe(self.send_queue.put_nowait,{
            'websocket': None,
            'message': Message('update_pv', {'pv': pv_name,
                                             'value': response.data[0]}, message_global=True)
        })



