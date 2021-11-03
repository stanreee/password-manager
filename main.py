from cryptography.fernet import InvalidToken
from account import Account
import json
import os.path
import constants
import util
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

key = None

def listAccounts():
    accounts = util.getAllAccounts()
    indexed_accounts = []

    index = 0
    for account in accounts:
        print(index, account['platform'])
        indexed_accounts.append(account)
        index += 1

    acc_index = input("Enter account index. Or type 'exit' to exit.")
    if acc_index == "exit":
        return
    acc_index = int(acc_index)
    acc = indexed_accounts[acc_index]

    state = ""
    while state != "exit":
        a = input("What would you like to do? \n1. Show password (show)\n2. Delete platform (delete)\n3. Exit (exit)")
        if a == "show":
            print("-----------------------------------------")
            print("| Account platform:", acc['platform'])
            print("| Email:", acc['email'])
            print("| Decrypted Password:", util.decryptPassword(acc['encrypted_password']))
            print("-----------------------------------------")
        elif a == "delete":
            try:
                util.decryptPassword(acc['encrypted_password'], throw=True)
            except InvalidToken:
                print("ERROR: The master password you entered is incorrect for this platform.")
                continue
            while a != "y" and a != "n":
                a = input("Are you sure you want to delete this platform? (y/n)")
                if a == "y":
                    accounts.pop(acc_index)
                    util.setJSONField(constants.accounts, accounts, "accounts")
                    print("Platform '" + acc['platform'] + "' deleted.")
                    state = "exit"
                elif a == "n":
                    state = "exit"
        elif a == "exit":
            state = "exit"

def addAccount():
    platform = input("Enter the platform name")
    email = input("Enter the email for this platform")
    password = input("Enter your password for this platform")

    acc = Account(platform, email, password)

    acc.saveAccountInfo()

    print("Account info for platform '" + platform + "' saved and the password has been encrypted.")

def setup():
    user = {}
    user['accounts'] = []

    with open(constants.accounts, "w") as outfile:
        json.dump(user, outfile)

def validateFiles():
    if not os.path.exists(constants.userData) and not os.path.exists(constants.accounts) or not os.path.exists(constants.accounts):
        return False
    return True

command = ""
while command != "exit":

    usedBefore = validateFiles()

    if not usedBefore:
        setup()
    
    if constants.key == "":
        verified = False
        password = input("Enter your master password. This password will be used to decrypt all other passwords. Do NOT forget this password, as all encrypted passwords will be lost.")

        encoded = password.encode()

        salt = constants.salt

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=10000
        )

        key = base64.urlsafe_b64encode(kdf.derive(encoded))

        constants.key = key

    command = input("What would you like to do? (exit, add, list)")
    if command == "list": listAccounts()
    elif command == "add": addAccount()


