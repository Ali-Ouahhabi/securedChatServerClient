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

# Instant messaging system Architecture
The architecture is based on a client server system for authentication and a client to client communication
## Server
With a  private and public keys
The server maintain a database  mapping usernames and hashed passwords 
The server permit to a user to sign up and authentify himself 
The server inform each connected client by any new connected or disconnected user and also a list of all connected client 
The server generate a symmetric key when a user want to communicate with another user, and communicate it to both users
## Client
 With the server public key
Client server Authentication
     ![Authentication and connexion anoucement](https://github.com/Ali-Ouahhabi/securedChatServerClient/blob/master/Ali%20Ouahhabi%20Problem%20set%203.svg)
* First Step: the client enter his username and password, the application will hash the password, and generate a symmetric key K, then send to the server Pubk[K]:K{USERNAME:Hash(Password)}

* Second Step: the server receive a new connection followed with the message Pubk[K]:K{USERNAME:Hash(Password)} with the server private key decrypt Pubk[K], then decrypted K{USERNAME:Hash(Password)}, check if the credential are in the database if it is the case send K{‘True’} otherwise send K{‘False’}
* Third step: user receive K{(‘False’|’True’)} decrypt the message if False ask the user to reenter the username and password and resend the authentication message to the server; otherwise if it is True it send back to the server the address of the Datagram Socket for peer client message 
## Client request to communicate with another user
![peer key generation](https://github.com/Ali-Ouahhabi/securedChatServerClient/blob/master/Ali%20Ouahhabi%20Problem%20set%203%20(1).svg)
When a user Y for the first time after his authentication, want to send a message to another connected user X:
* **Client Y** send a request to the server, for the address and a symmetric key to exchange secretly with X
* At the reception of this request by the **server**, it generate a key and send it back to both users X and Y 
* from the received server message **Client X** will know that he will be expecting a message from Y and therefore he has the key Kxy to decrypt the received message from Y and also to encrypt messages for Y
