from setuptools import setup, find_packages
setup(
    name="Epics-Websocket",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['websockets'],
    entry_points={
        'console_scripts':[
            'epicswebsocket = epics_websocket.scripts.start:start'
        ]
    }
)