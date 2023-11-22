from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64
from datetime import timedelta, datetime

##########################################################
#using hash functions, https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/
digest = hashes.Hash(hashes.SHA3_512()) #initialize SHA3-512 algorithm
messageToHash = "hello world" #alternately b"hello world" and you dont need the .encode() on the next line. 
digest.update(messageToHash.encode()) # feed data into the functions
hashValue = digest.finalize() #calculate the hash

print("hash is", base64.b64encode(hashValue).decode()) #print the hash encoded in base64

##########################################################
#Signature RSA key generation signing and verifying, https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

private_key = rsa.generate_private_key( #generate private key specific parameters 
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key() #get public key corresponding to the private key

private_key_as_pem = private_key.private_bytes( #serialize private key python object into bytes which can be store in a file
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.NoEncryption()
)

with open("privatekey.pem", "wb") as keyFile: #save private key in.a file
    keyFile.write(private_key_as_pem)

#similarly you can save public key into a file


with open("privatekey.pem", "rb") as keyFile: # read private key from a file
    private_key = serialization.load_pem_private_key(
        keyFile.read(),
        password=None,
    )



message = b"A message I want to sign"
signature = private_key.sign( #sign message 
    message,
    padding.PSS( 
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("signature is", base64.b64encode(signature).decode()) #print the hash encoded in base64

try: 
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

except InvalidSignature as e:
    print("Invalid signature, abort")

########################################################
#Creating (building) a certificate corresponding to the public key

builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([ 
    x509.NameAttribute(NameOID.COMMON_NAME, 'Bank'), # define the subject (the identity which owns the public key)
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, 'Certificate Authority'), #define the issuer (the certificate authority which signs this certificate)
]))

year = timedelta(365, 0, 0) #python time interval 

builder = builder.not_valid_before(datetime.today()) #set valid from date
builder = builder.not_valid_after(datetime.today() + year) #set expiration date
builder = builder.serial_number(x509.random_serial_number()) #random serial number (not important but necessary)
builder = builder.public_key(public_key) #the public key inside the certificate
builder = builder.add_extension(
    x509.BasicConstraints(ca=False, path_length=None), critical=True, #some extensions inserted into the certificate, not really important
)
certificate = builder.sign( #sign the certificate with the private key 
    private_key=private_key, algorithm=hashes.SHA3_256(),
)

print("our created certificate:", certificate)

certificateBytes = certificate.public_bytes(encoding=serialization.Encoding.PEM) #get serialized certificate which we can save into a file

with open("ourcert.crt", "wb") as certFile:
    certFile.write(certificateBytes)


with open("saved-cert.crt", "rb") as certFile:
    cert = x509.load_pem_x509_certificate(certFile.read()) #read certificate from a file
    print("loaded certificate", cert)


