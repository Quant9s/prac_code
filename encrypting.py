# from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# print(key)

# file = open('key.key', 'wb')
# file.write(key) #The key is type bytes
# file.close()

# file = open('key.key','rb')
# key = file.read()
# file.close()
# print(key)



import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = "abc" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes

salt = b';\x9e7\xdf\xbag\xd8\x02%4\x0cL+@?='
kdf = PBKDF2HMAC (
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
print(key)


from cryptography.fernet import Fernet

massage = "JisungKwon".encode()

f = Fernet(key)
encrypted = f.encrypt(massage)
print(encrypted)

from cryptography.fernet import Fernet
encrypted =b'gAAAAABcfqjVHPDYApdEfLCaCFfKz9bYRxXmk7qyxUcD0Igk63UFOSwQLDHcPM4-5MZhS5r7u8JHbqxjxgHM_qpOqnIKya8r0g=='

f = Fernet(key)
decrypted = f.decrypt(encrypted)
print(decrypted)



# from cryptography.fernet import Fernet
# from getpass import getpass
# key = b'ohGwXCCp4xIB87b7Utjn9ZELxQ5hSK0VrwccsgSxc6U='
# F_key = Fernet(key)
# user = {
#     'id'          : bytes(F_key.encrypt(input('user id: ').encode())),
#     'pw'          : bytes(F_key.encrypt(getpass('user pw: ').encode())),
#     'cert_pw'     : bytes(F_key.encrypt(getpass('user cert_pw: ').encode())),
#     'server_type' : str(0),
#     'show_error'  : str(0)}

# print(user['id'])
# print(user['pw'])
# print(user['cert_pw'])
# print(type(user['id']))
# print(type(user['pw']))
# print(type(user['cert_pw']))
# ###

# key = b'ohGwXCCp4xIB87b7Utjn9ZELxQ5hSK0VrwccsgSxc6U='
# user = {
#     'id'          : str(F_key.decrypt(user['id']).decode()),
#     'pw'          : str(F_key.decrypt(user['pw']).decode()),
#     'cert_pw'     : str(F_key.decrypt(user['cert_pw']).decode()),
#     'server_type' : str(0),
#     'show_error'  : str(0)}

# print(user['id'])
# print(user['pw'])
# print(user['cert_pw'])
# print(type(user['id']))
# print(type(user['pw']))
# print(type(user['cert_pw']))