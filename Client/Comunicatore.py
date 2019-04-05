import threading
import socket


class ServerCommunicator(threading.Thread):

    def __init__(self, connection_socket, server_request):
        threading.Thread.__init__(self)
        if isinstance(connection_socket, socket.socket):
            self.connection_socket = connection_socket
            self.max_size = 2024
            self.server_request = server_request

    def authentication(self, user, password):
        packet = "%s:%s" % (user, password)
        self.connection_socket.sendall(packet)
        return self.connection_socket.recv(2024)

    def sendUdpInfo(self, add):
        self.connection_socket.sendall(add)

    def recive(self):
        # may be length first the the list
        return self.connection_socket.recv(2024)

    def run(self):
        while True:
            req = self.connection_socket.recv(2024)
            self.server_request(req)

    def sendRequest(self, req):
        # message to server
        try:
            self.connection_socket.sendall(req)
        except Exception, o:
            raise Exception("cant send {}".format(o))


class UsersCommunicator(threading.Thread):

    def __init__(self, reference, in_contact):
        threading.Thread.__init__(self)
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection_socket.bind(('localhost', 0))
        self.reference = reference
        self.in_contact = in_contact
    def getaddinfo(self):
        add = self.connection_socket.getsockname()
        return self.connection_socket.getsockname()

    def run(self):
        while True:
            message, add = self.connection_socket.recvfrom(9000)
            tag = '%s%d' % add
            tag_ = self.reference[tag]
            message = self.in_contact[tag_]['secretary'].dec(message)
            print '[', tag_, '] said: ', message

    def sendto(self, message, info): # encryption
        address = info['address']
        secretary = info['secretary']
        message = secretary.enc(message)
        self.connection_socket.sendto(message, address)
