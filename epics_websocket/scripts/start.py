import argparse
from epics_websocket.server import start_server

def start():
    parser = argparse.ArgumentParser(description='Start EPICS/Websocket server.')
    parser.add_argument('--port', '-p', type=int, default=6064, help='Port number for websockets')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable Debugging Log')
    args = parser.parse_args()

    start_server(args.port, args.debug)

if __name__ == '__main__':
    start()