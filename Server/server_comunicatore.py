import threading
import socket
from secureTransactionF import SecureTransaction


class ServerCommunicator(threading.Thread):

    def __init__(self, connection, client_address, dataholder, prvk):
        threading.Thread.__init__(self)
        if isinstance(connection, socket.socket):
            self.connection = connection
            self.client_address = client_address
            self.dataholder = dataholder
            self.prvK = prvk
            self.secrecy = SecureTransaction(prv=prvk)

    def send(self, msg):
        try:
            msg = self.encrypt_request(msg)
            self.connection.sendall(msg)
        except Exception,o:
            print "ERROR", o

    def decrypte_authentication(self, request):
        request = request.split(':')
        k = self.secrecy.rsa_decrypt(request[0])
        self.secrecy.set_key(k)
        request = self.secrecy.dec(request[1])
        return request

    def encrypt_request(self, req):
        return self.secrecy.enc(req)

    def decrypt_request(self, req):
        return self.secrecy.dec(req)

    def authentication_request(self, request):
        form = self.decrypte_authentication(request)
        form = str(form).split(':')
        req = form[0]
        data = form[1:]

        if req == 'sign':
            test = self.dataholder.transaction.insert(data[0], data[1])
            resp = str(test)
            self.send(resp)
            return test, form[1]
        elif req == 'auth':
            test = self.dataholder.transaction.is_in(data[0], data[1])
            resp = str(test)
            self.send(resp)
            return test, form[1]
        else:
            raise Exception("request Unknown")
            return

    def reqeuestHandler(self, request):
        form = self.decrypt_request(request)
        form = str(form).split(':')
        req = form[0]
        data = form[1:]
        if req == 'user':
            if data[0] in self.dataholder.clients_udp_address:
                k = SecureTransaction.generate_key()
                ip, port = self.dataholder.clients_udp_address[self.corespondant]
                ip = ip.replace("'", "")
                msg = "user:%s:%s:%s" % (self.corespondant, k, "%s,%s" % (ip, port))
                self.dataholder.clients_tcp_sockets[data[0]].send(msg)
                ip, port = self.dataholder.clients_udp_address[data[0]]
                ip = ip.replace("'", "")
                msg = "user:%s:%s:%s" % (data[0], k, "%s,%s" % (ip, port))
                k = 0
            else:
                msg = "Nuser:%s" % data[0]
        elif req == 'list':
            if len(self.dataholder.clients) != 0:
                msg = self.dataholder.clients
                msg = "list:%s" % ','.join(msg)
            else:
                msg = "empty"
        self.send(msg)

    def run(self):
        try:
            while True:
                aut = self.connection.recv(9000)
                authentificationtest, aut = self.authentication_request(aut)
                if authentificationtest:
                    break
        except:
            return
        try:
            if not authentificationtest:
                # try to blacklist the user for a timeout
                # .....???????
                pass
            else:
                # o get udp info
                udpinfo = self.connection.recv(4096)
        except:
            return
        self.corespondant = aut
        self.dataholder.clientConected(self, aut, udpinfo.split(','))

        while True:
            try:
                print "..."
                req = self.connection.recv(4096)
                self.reqeuestHandler(req)
            except Exception,o:
                print "ERROR", o
                self.dataholder.clientDisconected(aut)
                return
