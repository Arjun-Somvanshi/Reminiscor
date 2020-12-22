from security import *

def signup_response(username, password, c_password):
    result = [1,1,1]
    if len(username)<3:
        result[0] = 0
    elif len(password)<8:
        result[1] = 0
    elif password != c_password:
        result[2] = 0
    username = None
    password = None
    c_password = None
    return result

def on_sucess_signup(username, password, keyfile = False):
    key2 = None
    write_remfile(write = True) # initializing the rem file
    write_remfile('username.txt', username)
    write_AppConfig(keyfile) # writing the configs to run argon2
    password_hash = blake(password) # this is the hash from the password 
    if keyfile:
        key2 = keyfile_encryption(password_hash.encode('utf-8')) # if key file is there then it's generated
    m_key = master_key(key1 = password_hash, key2 = key2, first = True)
    master_key_store(m_key)
    print('master key: ', m_key)
    m_key = None
    password_hash = None
    key2 = None
    password = None

def login_auth(master_password, keyfile_dir):
    hash_of_master = blake(master_password)
    print(hash_of_master)
    if keyfile_dir != None:
        key2 = keyfile_decrypt(hash_of_master.encode('utf-8'), keyfile_dir)
        m_key = master_key(key1=hash_of_master, key2=key2)
        result = auth_hash(m_key)
    else:
        m_key = master_key(key1 = hash_of_master, key2 = None)
        result =  auth_hash(m_key)
    return [result, m_key]
