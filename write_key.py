
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

key_passwd_provided = "JKwon" # This is input in the form of a string
key_passwd = key_passwd_provided.encode() # Convert to type bytes

'''
import os
os.urandom(16)
'''
salt = b'\xd7J\xd3\xd6sk\xdb\x97\xf5\xa7\xf2-m\xcf\xc6\xbd'
kdf = PBKDF2HMAC (
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(key_passwd)) # Can only use kdf once

file = open('key.key','wb')
file.write(key)
file.close