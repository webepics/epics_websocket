import logging
from .epics_protocol import EpicsServerProtocol

def start_server(port=6064, debug=False):
    """ Start the Websocket server """
    logging.basicConfig(level=logging.DEBUG)
    epics_server = EpicsServerProtocol(port=port, debug=debug)
    epics_server.run()


if __name__ == '__main__':
    start_server()