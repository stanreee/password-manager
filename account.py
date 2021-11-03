import json
from cryptography.fernet import Fernet
import constants
import os
import util

class Account:

    def __init__(self, platform, email, password) -> None:
        self.platform = platform
        self.email = email
        self.encrypted_pass = self.encryptPass(password)

    def getPlatform(self):
        return self.platform

    def getEmail(self):
        return self.email

    def getEncryptedPass(self):
        return self.encrypted_pass

    def setEmail(self, email):
        self.email = email

    def saveAccountInfo(self):
        util.appendToFile(constants.accounts, self.convertToDict(), "accounts")

    def encryptPass(self, password):
        key = constants.key

        f = Fernet(key)

        encrypted = f.encrypt(password.encode())

        return encrypted

    def convertToDict(self):
        dictionary = {
            "platform" : self.platform,
            "email": self.email,
            "encrypted_password": self.encrypted_pass.decode()
        }
        return dictionary

    def convertDictToObj(self, dictionary):
        return Account(dictionary.platform, dictionary.email, dictionary.encrypted_password)
