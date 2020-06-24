import pbkdf2
import os

salt = os.urandom(8)    # 64-bit salt
print(salt)
print('\n\n')
key = pbkdf2.PBKDF2("This passphrase is a secret.", salt).read(32) # 256-bit key
key1 = pbkdf2.PBKDF2("This passphrase is a secret.", salt).read(32) # 256-bit key
print(key)
print('\n\n')
print(key1)
