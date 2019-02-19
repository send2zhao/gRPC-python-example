import grpc

import time
import random
import sys
from concurrent import futures
import AddressBook_pb2
import AddressBook_pb2_grpc

from google.protobuf import json_format


# https://grpc.io/docs/tutorials/basic/python.html


class AddressService(AddressBook_pb2_grpc.AddressBookServiceServicer):

    def _create_response(count=1, name="Hui"):
        addressBook = AddressBook_pb2.AddressBook()

        # create a entry
        for i in range(count):
            address = AddressBook_pb2.Address(
                name=name + "-" + str(i),
                age=100,
                address="100 Cherry Street"
            )
            addressBook.book.extend([address])
        
        return addressBook

    def _create_response_list():
        for i in range(4):
            addressBook = AddressBook_pb2.AddressBook()
            address = AddressBook_pb2.Address(
                name="No. " + str(i),
                age=1+i,
                address="199 Cherry Street"
            )
            addressBook.book.extend([address])
            yield addressBook
            time.sleep(random.uniform(0.5, 1.0))

    def Get(self, request, context):
        print('[Get] received ' + json_format.MessageToJson(request))
        print('[Get] send response back.')
        return AddressService._create_response()

    def GetSimple(self, request, context):
        print('[GetSimple] recived ' + json_format.MessageToJson(request))
        print('[GetSimple] send response back.')
        return AddressService._create_response()

    def GetStream(self, request, context):
        # return stream
        responseList = AddressService._create_response_list()
        print('[GetStream] receiving request. Sendback stream.')
        for item in responseList:
            print('(send).', end='')
            sys.stdout.flush()
            time.sleep(3)
            yield item  # using yield
        
    def SendStream(self, request_iterator, context):
        count = 0
        print('[SendStream] Receiving stream.')
        start_time = time.time()
        for item in request_iterator:
            count += 1
            print('[SendStream] recieving streaming request item.')

        elapsed_time = time.time() - start_time
        print('Elapsed time: ' + str(elapsed_time))
        print('[SendStream] send resoponse back.')
        return AddressService._create_response(count)

    def ChatAPI(self, request_iterator, context):
        print('[ChatAPI] receiving request stream.')
        for request in request_iterator:
            print('[ChatAPI] Received: ' + json_format.MessageToJson(request))
            name = request.name
            print('[ChatAPI] Send back response.')
            yield AddressService._create_response(name=name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    AddressBook_pb2_grpc.add_AddressBookServiceServicer_to_server(AddressService(), server)

    server.add_insecure_port('[::]:50052')
    server.start()

    try:
        while True:
            time.sleep(20000)
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    serve()


