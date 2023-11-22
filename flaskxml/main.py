from flask import Flask
from flask import render_template

from idp.idpFunctions import *
from lxml import etree


app = Flask(__name__)

idpPrefix = "/idp"
bankPrefix = "/bank"

#list of namespaces that are inside AuthnRequest - needed for XPath search inside the XML document
XMLnamespaces = {
    'saml2p': 'urn:oasis:names:tc:SAML:2.0:protocol',
    'saml2': 'urn:oasis:names:tc:SAML:2.0:assertion',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

#this will run when you go to http://127.0.0.1:5000/
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" 

#this will run when you go to http://127.0.0.1:5000/idp/login
@app.route(idpPrefix + "/login")
def loginTest():
    testVar = "helloworld"
    listOfVariables = {
        "var1": 123,
        "xmlContent" : "i dont know",
        "var2" : testVar
    }
    print(listOfVariables)

    return render_template("hello.html", variables=listOfVariables) #render template from templates/hello.html with variables that are in listOfVariables


#this will run when you go to http://127.0.0.1:5000/bank
@app.route("/bank")
def bank():
    return render_template("bank.html") #xass


#this will run when you go to http://127.0.0.1:5000/idp
@app.route("/idp")
def idp():
    return printResponseForIdp() #calling function outside of this file


#this will run anywhere except those that are already defined (/idp, /bank etc.) and it will treat everything after / in the URL as a variable called "username"
@app.route('/<username>')
def show_user(username):
    print(username)
    return "user is " + username

#this runs when you go to http://127.0.0.1:5000/xml
@app.route('/xml')
def xml():
    filePath = "files/exampleSAMLAuthnRequest.xml"
    tree = etree.parse(filePath) #read, load and parse the file into memory
    root = tree.getroot() #get Element variable (instead of a ElementTree variable). This is needed for xpath function call

    digestValueElement = root.xpath("//ds:DigestValue", namespaces = XMLnamespaces)[0] #returns the first element that is <ds:DigestValue>
    #listOfDigestValueElements = root.xpath("//ds:DigestValue", namespaces = XMLnamespaces) #this would return a list of all elements <ds:DigestValue>

    digestValue = digestValueElement.text #get the text inside the element

    return "digest value is " + digestValue

