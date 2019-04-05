import socket
from Comunicatore import ServerCommunicator, UsersCommunicator
from secureTransactionF import SecureTransaction

import yaml
import os

class client:

    def __init__(self, config):
        self.config = config
        self.username = None
        self.clients = []
        self.reference = {}
        self.in_contact = {}
        self.udpcom = None
        self.server = None
        self.tempMessg = {}
        self.cmd = ['list', 'send USER MESSAGE', 'STOP', 'HELP']
        self.secrecy = self.init_secrecy(self.config['server_certificate'])

    def init_secrecy(self, path):
        stmp = SecureTransaction.generate_key()
        astmp = SecureTransaction.get_pub_key(path)
        return SecureTransaction(key=stmp, pub=astmp)

    def handel_authentification(self, *auth):
        auth = auth[1]
        auth[2] = self.secrecy.hash_password(auth[2])
        if auth[0] == 'auth':
            msg = ':'.join(auth)
        elif auth[0] == 'sign':
            msg = ':'.join(auth)
        else:
            raise Exception('undefined auth')
            return
        msg = self.encrypt_authentication(msg)
        self.server.sendRequest(msg)
        resp = self.server.connection_socket.recv(9000)
        return self.decrypt_request(resp)

    def server_request(self, req):
        req = self.decrypt_request(req)
        req = req.split(':')
        if req[0] == 'conected':
            if req[1] in self.clients:
                pass
            else:
                print ">user connected ! >>:", req[1]
                self.clients.append(req[1])
        elif req[0] == 'disconected':
            print ">user disconnected ! >>:", req[1]
            if req[1] in self.clients:
                self.clients.remove(req[1])
                if req[1] in self.in_contact:
                    self.in_contact.pop(req[1])
            else:
                pass
        elif req[0] == 'list':
            if req[1] != "empty":
                resp = req[1].split(',')
                self.clients = resp
                self.clients.remove(self.username)
            else:
                print "\n", ">resp: list <", "no user connected"
                self.clients = []

            print ">connected users ! >>", self.clients
        elif req[0] == 'user':
            resp = req[3].split(",")
            resp[1] = int(resp[1])
            ss = SecureTransaction(key=req[2])
            self.in_contact[req[1]] = {'address': tuple(resp),
                                       'secretary': ss
                                       }
            tag = '%s%s' % (resp[0], resp[1])
            self.reference[tag] = req[1]
            if req[1] in self.tempMessg:
                msg = self.tempMessg.pop(req[1])
                self.udpcom.sendto(msg, self.in_contact[req[1]])
        elif req[0] == 'Nuser':
            print "unfounded user", req[1]
        else:
            print "unkown request from server", req

    def handel_request(self, request):
        info = request.split()
        if len(info) == 1 and info[0] == 'list':
            req = "list:"
            req = self.encrypt_request(req)
            self.server.sendRequest(req)
        elif len(info) >= 3 and info[0] == 'send':
            if info[1] in self.in_contact:
                self.udpcom.sendto(' '.join(info[2:]), self.in_contact[info[1]])
            else:
                req = "user:%s" % info[1]
                self.tempMessg[info[1]] = ' '.join(info[2:])
                req = self.encrypt_request(req)
                self.server.sendRequest(req)

    def encrypt_authentication(self, msg):
        t = self.secrecy.rsa_crypt(self.secrecy.key)
        d = self.secrecy.enc(msg)
        msg = "%s:%s" % (t, d)
       # msg = base64.b64encode(msg)
        return msg

    def encrypt_request(self, req):
        return self.secrecy.enc(req)

    def decrypt_request(self, req):
        return self.secrecy.dec(req)

    def udp_serve(self, ):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def establish_connexion(self, ip='localhost', port=0):
        # type: (str, int) -> socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.config['server_address'], self.config['server_port'])
        self.sock.connect(server_address)
        return self.sock

    def main(self):
        # establish connection:
        cnx = self.establish_connexion()

        self.server = ServerCommunicator(connection_socket=cnx, server_request=self.server_request)

        print "(auth|sign) USERNAME PASSWORD"
        while True:
            auth = raw_input().split()
            if len(auth) == 3 and auth[0] in ('auth', 'sign'):
                resp = self.handel_authentification(self, auth)
                if resp == 'True':
                    self.username = auth[1]
                    self.udpcom = UsersCommunicator(self.reference, self.in_contact)
                    self.udpcom.start()
                    self.server.sendUdpInfo(str(self.udpcom.getaddinfo()).strip('()'))
                    self.server.start()
                    self.handel_request("list")
                    break
                else:
                    if auth[0] == 'auth':
                        print "authentication failed"
                    elif auth[0] == 'sign':
                        print "sign up failed"
            else:
                print "unexpected command"

        connected = True
        while connected:
            req = raw_input()
            if req == "STOP":
                break
            elif req == "HELP" or req == '?':
                print self.cmd
            else:
                self.handel_request(req)


if __name__ == "__main__":
    if os.path.exists('./config.yaml'):
        config_file = open('./config.yaml', 'r')
        load = yaml.safe_load_all(config_file)
        config = load.next()
        if config['server_address']:
            pass
        else:
            print "configuration file messing server address"

        if config['server_port']:
            pass
        else:
            print "configuration file messing server port number"

        if config['server_certificate']:
            if os.path.exists(config['server_certificate']):
                pass
            else:
                print "certificate path unresolved"
        else:
            print "configuration file messing server certificate file path"
        client(config).main()
    else:
        print "can't find configuration file"
