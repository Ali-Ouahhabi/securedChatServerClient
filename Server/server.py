import socket
import sys
from server_comunicatore import ServerCommunicator
from persistent import transaction
from secureTransactionF import SecureTransaction
import os,yaml


class SharedDataHolder:
    #synco

    clients_tcp_sockets = {}
    clients_udp_address = {}
    clients = []
    transaction = None

    @staticmethod
    def clientConected(worker, client, udpinfo):
        msg = "conected:%s" % client
        for k in SharedDataHolder.clients_tcp_sockets:
            SharedDataHolder.clients_tcp_sockets[k].send(msg)
        SharedDataHolder.clients.append(client)
        SharedDataHolder.clients_tcp_sockets[client] = worker
        SharedDataHolder.clients_udp_address[client] = udpinfo

    @staticmethod
    def clientDisconected(client):
        if client in SharedDataHolder.clients:
            SharedDataHolder.clients.remove(client)
        if client in SharedDataHolder.clients_tcp_sockets:
            SharedDataHolder.clients_tcp_sockets.pop(client)
        if client in SharedDataHolder.clients_udp_address:
            SharedDataHolder.clients_udp_address.pop(client)
        msg = "disconected:%s" % client
        for k in SharedDataHolder.clients_tcp_sockets:
            SharedDataHolder.clients_tcp_sockets[k].send(msg)

def main(config):
    print config
    SharedDataHolder.transaction = transaction(config['data_base'])
    prvk = SecureTransaction.get_prv_key(config['server_privateKey'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (config['server_address'], config['server_port'])
    sock.bind(server_address)
    sock.listen(2)
    while True:
        # Wait for a connection
        print >> sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        print "connection type ::>>", type(connection)
        w = ServerCommunicator(connection, client_address, SharedDataHolder, prvk=prvk)
        print "client connected ", client_address
        nc = '%s:%s' % client_address
        w.start()


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

        if config['server_privateKey']:
            if os.path.exists(config['server_privateKey']):
                pass
            else:
                print "privateKey path unresolved"

        if config['data_base']:
            if os.path.exists(config['server_certificate']):
                pass
            else:
                print "data base unresolved"

        else:
            print "configuration file messing server certificate file path"
        main(config)
    else:
        print "can't find configuration file"
