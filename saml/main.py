import urllib.parse
import base64
from lxml import etree
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509




XMLnamespaces = {
    'saml2p': 'urn:oasis:names:tc:SAML:2.0:protocol',
    'saml2': 'urn:oasis:names:tc:SAML:2.0:assertion',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

with open("files/encodedAuthnRequest.txt", "r") as file:
    line = urllib.parse.unquote(file.readline()) # first decode from URL encoding
    decodedString = base64.b64decode(line) # second decode from Base64 encoding
    root = etree.fromstring(decodedString) # parse the XML document in decodedString
    digestValueElement = root.xpath("//ds:DigestValue", namespaces = XMLnamespaces)[0] #find the DigestValue element
    digestValue = digestValueElement.text #get the text content of that element (the encoded digest)
    # print(digestValue)

    signatureEl = root.xpath("//ds:Signature", namespaces = XMLnamespaces)[0] #find the Signature element
    # print(signatureEl)


    root.remove(signatureEl) #remove it before calculating the document digest

    xmlString = etree.tostring(root, method="c14n", with_comments=False, exclusive=True) #serialize the document (the whole AuthnRequest element) (without the signature element) into a string using the format "c14n exclusive and no comments"
    # print(xmlString.decode("utf-8"))

    digest = hashes.Hash(hashes.SHA1()) #initialize the hash function
    digest.update(xmlString) #input the data into the hash function
    hashValue = digest.finalize() #get the hash result
    print(base64.b64encode(hashValue).decode()) #encode the hash (in bytes) into a Base64 string

    root.insert(1,signatureEl) #insert the element back because the xpath() function did not work on signatureEl

    signatureValue = root.xpath("//ds:SignatureValue", namespaces = XMLnamespaces)[0].text #get the SignatureValue content 
    signedInfo = root.xpath("//ds:SignedInfo", namespaces = XMLnamespaces)[0] #get the SignedInfo element
    encodedCertificate = root.xpath("//ds:X509Certificate", namespaces = XMLnamespaces)[0] #get the X509Certificate element

    certificateString = encodedCertificate.text #get the encoded certificate
    pemCertificateString = "-----BEGIN CERTIFICATE-----\n" + certificateString + "\n-----END CERTIFICATE-----" #modify the encoded certificate string so it is in the "PEM" format
    cert = x509.load_pem_x509_certificate(pemCertificateString.encode()) #parse the encoded certificate
    publicKey = cert.public_key() #get the public key from the certificate

    message = etree.tostring(signedInfo, method="c14n", with_comments=False, exclusive=True) #serialize the SignedInfo element into a string

    publicKey.verify(
        base64.b64decode(signatureValue), #signature value which we are checking, the signature is decoded from Base64 string to bytes
        message, #message which should correspond to the signature
        padding.PKCS1v15(), #the signature algorithm parameter (RSA PKCS1.5)
        hashes.SHA256() #the hash function used inside the signature algorithm (to hash the message)
    ) #signature didnt throw exception, it is valid




