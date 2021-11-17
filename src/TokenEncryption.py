#!/usr/bin/env python

import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

'''
Created by Adi Shastry
Email: ams2590@columbia.edu
'''

class TokenEncryptor:
    '''
        This class is meant to handle the storage, retrieval, and creation
        of encrypted passwords.
    '''
    def __init__(self,createNewJson=False, encryptedTokenLoc="TODO:add the location "):
        '''
        Initialize the Token Encryptor
        Inputs:
            - encryptedTokenLoc: Holds the full file path of the json file with 
                                        users and encrypted passwords.
            - createNewJson: Boolean to create a new file. Set as false if you 
                            are trying to set up a new database of encrypted
                            tokens
        Outputs:
            - None
        '''
        self.createNewJson = createNewJson
        self.encryptedTokenLoc = encryptedTokenLoc
    def addUsers(self):
        '''
        Method will add a new user to the token and password database
        Inputs:
            - 
        Outputs:
            - Status String
        '''
        #Take in the User's Username, password and token
        username = input("Enter a Username:")
        token = input("Enter the API token you want to encrypt")
        password = input("Enter a password to encrypt the token with")

        #We want to encrypt the the token with the password
            #TODO: Check the article where they show how to do this

        #Check if we indeed have a file or if we need to make a new one
        if not self.createNewJson:
            #Then we want to create a new file
        password = password_provided.encode()  # Convert to type bytes
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once



    #TODO: Method to remove users

    #TODO: Method to decrypt and return tokens, given username and password

 
