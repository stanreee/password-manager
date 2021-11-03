import json
import nacl.pwhash
import nacl.utils
import os
import constants
from cryptography.fernet import Fernet, InvalidToken

def setJSONField(jsonFile, data, field):
    json_obj = {}
    with open(jsonFile, 'r') as outfile:
        json_obj = json.load(outfile)

    json_obj[field] = data

    with open(jsonFile, "w") as outfile:
        json.dump(json_obj, outfile)

def appendToFile(jsonFile, data: dict, field):
    json_obj = {}
    with open(jsonFile, 'r') as outfile:
        json_obj = json.load(outfile)

    json_obj[field].append(data)

    with open(jsonFile, "w") as outfile:
        json.dump(json_obj, outfile)

def getAccountInfo(account_obj):
    json_obj = {}
    with open(constants.accounts, 'r') as outfile:
        json_obj = json.load(outfile)

    accounts = json_obj["accounts"]

    for account in accounts:
        if account["platform"] == account_obj.getPlatform():
            return account
    return -1

def getAllAccounts():
    json_obj = {}
    with open(constants.accounts, 'r') as outfile:
        json_obj = json.load(outfile)

    accounts = json_obj["accounts"]
    return accounts

def decryptPassword(encrypted_password, throw=False):
    f = Fernet(constants.key)
    try:
        decrypted = f.decrypt(encrypted_password.encode())
    except InvalidToken:
        if throw:
            raise InvalidToken
        return "ERROR: INVALID_MASTER_PASSWORD"
    return decrypted

def derive_key(password):
    return nacl.pwhash.argon2id.kdf(nacl.pwhash.argon2id.BYTES_MAX, bytes(password, 'utf-8'), nacl.utils.random(16))