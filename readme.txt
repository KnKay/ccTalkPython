This is a simple ccTalk package.

The bus will handle the real communication over the wire.
This is at the moment controlled by the class.
We only read the bus once we call the method.
This approch is ok as we tend to be the master.
This will not work once we try to be a unit!

During first approach only the simple checksum is used

Plans to be implemented:
- Build terminal to test a connected device
- Build a sniffer
- Build some devices to interact with real hardware



Installation
==============

pip install -r requirements.txt


