# Module for security protocols of reminiscor

'''
Following is the way to define argon two parameters:
    * set the number of iteration to 2
    * choose how many devices you will use the database on, and note the ram of the device which has the least memory, let that be m
    * the memory parameter should be the least of m/2 and 1
    * Find out the number of logical processors of each of your devices. Set the parallelism parameter to the minimum of these numbers. On Windows 10, 
      the number of logical processors can be found in the Task Manager (right-click onto the taskbar → 'Task Manager') on the 'Performance' tab page.
'''

import hashlib
from Crypto.Random import get_random_bytes
import json
import argon2
from FileHandling import *
from base64 import b64encode, b64decode
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def blake (data): # send strings or bytes
    if type(data) == str:
        data = data.encode('utf-8')
    hash1 = hashlib.blake2b(data)
    data = None # unassigning the value of data
    return hash1.hexdigest()

def keyfile_encryption(key1):
    keyfile_data = get_random_bytes(16)
    keyfile_cipher = ECB_encrypt(keyfile_data, key1[:16])
    with open(HomeDir('KeyFile.dat', 'UserData'), 'wb') as f:
        f.write(keyfile_cipher)
    return keyfile_data

def keyfile_decrypt(key1):
    with open(HomeDir('KeyFile.dat', 'UserData'), 'rb') as f:
        keyfile_cipher = f.read() 
    keyfile_data = ECB_decrypt(keyfile_cipher, key1[:16])
    return keyfile_data

def master_key(key1, first = False, re_encrypting = False, key2 = None): #used to derive the master key from argon 2 using keyfile and master password
    # read the argon2 parameters before kdf
    param = json.loads(read_remfile('app_config.json'))
    print ('these are the configurations:', param)
    # gotta get random salt only when database is re-encrypted
    if first or re_encrypting: # re_encrypting should be true when reencrypting the database
        salt = get_random_bytes(16)
        write_remfile('master_salt.bin', salt)
    else:
        salt = read_remfile('master_salt.bin') # reading the defined salt
    
    if key2 is not None: # incase there is no keyfile involved
        print('password hash: ', key1,'\nkeyfile: ', key2)
        composite_key = key1[:16] + key2[:16]
    
    else:
        composite_key = key1[:32]
    #unassigning the sensitive data
    key1 = None
    key2 = None
    composite_key = composite_key.encode('utf-16')
    #print(composite_key) uncomment to test the compostie key value
    #print(salt)
    masterkey = argon2.low_level.hash_secret_raw(secret = composite_key, 
                                                 salt = salt, 
                                                 time_cost = param['argon2_settings']['time_cost'], 
                                                 memory_cost=param['argon2_settings']['memory_cost'], 
                                                 parallelism= param['argon2_settings']['parallelism'], 
                                                 hash_len = 32, 
                                                 type=argon2.Type.D, 
                                                 version=19)# deriving the AES KEY for data base
    #unassigning the sensitive data
    composite_key = None
    return masterkey

def master_key_store(master_key): # This stores the master key's hash value
    key_hash = blake(master_key)
    write_remfile('master_key_hash.bin', key_hash.encode('utf-8'))

def auth_hash(master_key):
    key_hash = blake(master_key) 
    stored_hash = read_remfile('master_key_hash.bin').decode('utf-8')
    if key_hash == stored_hash:
        return True
    return False

def ECB_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(plaintext)
    return ct

def ECB_decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(cipher_text)
    return pt

def AES_Encrypt(key, data): # The data should be in bytes here
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    iv = b64encode(ECB_encrypt(cipher.iv, key)).decode('utf-8')
    encrypted_data = {'iv': iv, 'ct': ct}
    return encrypted_data

    
def AES_Decrypt(key, encrypted_data): # enrypted_data is a dictionary which contains the encrypted form of the iv and the encrypted data
    iv = ECB_decrypt(b64decode(encrypted_data['iv']), key) # decoding from base64 and then getting the iv back by decrypting it
    ct = b64decode(encrypted_data['ct'])
    cipher = AES.new(key, AES.MODE_CBC, iv = iv )
    pt_bytes = unpad(cipher.decrypt(ct), AES.block_size)
    return pt_bytes

'''this function is for testing the key generation'''
def composite_key_test(first):
    k1 = blake('manu')
    k2= blake('arjun')
    return master_key(key1 = k1,key2 = k2, first = first)

def test_encryption(): # to test the encryption
    database = {'entries':{'username': 'arjun somvanshi', 'password': 'arjun2000123455667'}}
    database_as_bytes = json.dumps(database).encode('utf-8')
    print(database_as_bytes)
    key = composite_key_test(False)
    e_data = AES_Encrypt(key, database_as_bytes)
    print(e_data['iv'],'\n',e_data['ct'])
    d = AES_Decrypt(key, e_data)
    print(json.loads(d))
    '''tester = get_random_bytes(32)
    print(key, '\n', tester, sys.getsizeof(key), sys.getsizeof(tester))'''

# Creat a user here and do tests
'''write_remfile(write=True)
write_AppConfig()
key = composite_key_test(True)
key1 = get_random_bytes(32)
master_key_store(key)
print(auth_hash(key1))'''
