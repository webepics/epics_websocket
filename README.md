# epics_websocket

Python EPICS to websocket connector.

## Installation

```bash
$ git clone https://github.com/webepics/epics_websocket.git
$ cd epics_websocket
$ python setup.py install
```

## Run Server

To run on default port, 6064, without debugging logs:

```
$ epicswebsocket
```

Help on command:
```
$ epicswebsocket -h
usage: epicswebsocket [-h] [--port PORT] [--debug]

Start EPICS/Websocket server.

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  Port number for websockets
  --debug, -d           Enable Debugging Log
```

