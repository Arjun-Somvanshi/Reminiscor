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
    set_username(username)
    write_remfile(write = True) # initializing the rem file
    write_AppConfig() # writing the configs to run argon2
    password_hash = blake(password) # this is the hash from the password 
    if keyfile:
        key2 = keyfile_encryption(password_hash.encode('utf-8')) # if key file is there then it's generated
    m_key = master_key(key1 = password_hash, key2 = None, first = True)
    master_key_store(m_key)
    m_key = None
    password_hash = None
    key2 = None
    password = None

def login_auth(master_password):
    pass

