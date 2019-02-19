##

See https://grpc.io/docs/tutorials/basic/python.html.


### Installation

Install gPRC:
```bash
python -m pip install grpcio
```

Install gPRC tools, run:
```bash
python -m pip install grpcio-tools
```


###

1. Create proptocol buffer file
2. Build gRPC code.
3. Implement the APIs.
4. Run the server/client program.


#### Create protocol buffer file
Define the message, and service using Protocol Buffer format. Generate proto file `AddressBook.proto`.


#### Build the gRPC code
```
build.bat
```

#### Implement APIs

Write `myServer.py`, and  `myClient.py` following the definition in `AddressBook.proto`.


#### Run server and client

Start the server.
```bash
python myServer.py
```

Run the client.
```bash
python myClient.py
```

