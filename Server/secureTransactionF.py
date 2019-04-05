from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import bcrypt
import base64


class SecureTransaction:

    def __init__(self, key=None, pub=None, prv=None):
        if key:
            self.cipher = Fernet(key)
        else:
            self.cipher = None
        self.prv = prv
        self.pub = pub
        self.key = key
        self.padding_ = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )

    def rsa_crypt(self, msg):
        if self.pub:
            return base64.b64encode(self.pub.encrypt(msg, self.padding_))
        else:
            raise Exception('no public Key')

    def rsa_decrypt(self, msg):
        if self.prv:
            msg = base64.b64decode(msg)
            return self.prv.decrypt(msg, self.padding_)
        else:
            raise Exception('no private key')

    def enc(self, msg):
        if self.cipher:
            return base64.b64encode(self.cipher.encrypt(msg))
        else:
            raise Exception('no symmetric Key')

    def dec(self, msg):
        if self.cipher:
            msg = base64.b64decode(msg)
            return self.cipher.decrypt(msg)
        else:
            raise Exception('no symmetric Key')

    def set_key(self, key):
        self.key = key
        self.cipher = Fernet(key)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def get_pub_key(path):
        try:
            public_key_data = open(path, "r").read()
            key = x509.load_pem_x509_certificate(public_key_data, default_backend()).public_key()
            if isinstance(key, rsa.RSAPublicKey):
                return key
            else:
                raise Exception(" private key error")
        except Exception, o:
            raise Exception("File {} was not found \n {}".format(path, o))

    @staticmethod
    def get_prv_key(path):
        try:
            private_key_data = open(path, "r").read()
            key = load_pem_private_key(private_key_data, password=None, backend=default_backend())
            if isinstance(key, rsa.RSAPrivateKey):
                return key
            else:
                raise Exception(" private key error")
        except Exception, o:
            raise Exception("File {} was not found \n {}".format(path, o))

    def hash_password(self, msg):
        return bcrypt.hashpw(password=b'password', salt=b'QS5MLkkulNmI2YfYp9io2Yog')
