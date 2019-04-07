# securedChatServerClient
An application developed with python 2.7, for a secure communication between clients, the server in this application authenticated users, and generation symmetric keys for peer users communication

## Execution example
### starting the server
    python ./Server/server.py 

### starting the client
    python ./Client/client.py 
## the CLI handeled by the client application
##### authentication
    auth USERNAME PASSWORD
##### signing up
    sign USERNAME PASSWORD
##### sending a message to userX
    send userX message
##### requesting the list of connected users
    list

## The packacges used in this aplication 
**cryptography** with fernet for key generation and message encryption/decryption also RSA for key encryption

**bcrypt** for password hashing

**tinyDB** to store username's and passwords in a json file

**PyYaml** to read configuration file

**socket** for network communication TCP dadatgram betweend client and server and UDP datagrame between clients

## Configuration Files 
### client configuration file 
specify the ip address and the location of the server certificate 

    cat /Client/config.yaml
    server_address: localhost
    server_port: 10000
    server_certificate: ./KeyA_/A_certificate.crt
    
### server configuration file
sepecify the ip address of the server, the location of it public and private keys, and the json file were are the passwords stored

    cat /Server/config.yaml
    server_address: localhost
    server_port: 10000
    server_certificate: ./KeyA/A_certificate.crt
    server_privateKey: ./KeyA/A_privateKey.key
    data_base: pass.json

