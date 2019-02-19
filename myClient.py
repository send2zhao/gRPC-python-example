from __future__ import print_function
import logging

import grpc
import time
from concurrent import futures

import AddressBook_pb2
import AddressBook_pb2_grpc


from google.protobuf import json_format


def generate_requestList(count=4):
    for i in range(count):
        message = AddressBook_pb2.AddressBookRequest(name=str(i+1))
        print('sending : ' + json_format.MessageToJson(message))
        yield message
        time.sleep(1)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = AddressBook_pb2_grpc.AddressBookServiceStub(channel)
        
        print('===[Get]===')
        response = stub.Get(AddressBook_pb2.AddressBookRequest(name='you'))
        print("Greeter client received: " + json_format.MessageToJson(response))

        time.sleep(4)
        print('===[GetSimple]===')
        response = stub.GetSimple(AddressBook_pb2.Empty())
        print("Simple: " + json_format.MessageToJson(response))

        print('===[GetStream]===')
        print('streaming receiving message')
        for item in stub.GetStream(AddressBook_pb2.Empty()):
            print('Streaming: ' + json_format.MessageToJson(item))

        print('===[SendStream]===')
        print('streaming requests')
        requestList = generate_requestList()
        response = stub.SendStream(requestList)
        print('Streaming request response: ' + json_format.MessageToJson(response))

        print('===[ChatAPI]===')
        requestList = generate_requestList()
        responseList = stub.ChatAPI(requestList)
        for response in responseList:
            print('chat response: ' + json_format.MessageToJson(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()
