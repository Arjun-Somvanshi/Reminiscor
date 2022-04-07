'''
Reminiscor is a free offline password manager.
Copyright (C) 2020 Arjun Somvanshi & Manvendra Somvanshi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
from security import *
import re
import pickle
class api():
    def isalnum_with_space(self, string):
        wordlist = string.split(' ')
        print(wordlist)
        for word in wordlist:
            if word.isalnum:
                pass
            else:
                return False
        return True 
    def check_user(self):
        rem_exists = False
        try:
            for fname in os.listdir(HomeDir('', 'UserData')):
                if fname.endswith('master_key_hash.bin'): #if master key hash file exists then signup won't be called
                    print("Master Key Hash Bin is found :(")
                    rem_exists = True
                    break
        except:
            rem_exists = False
        return rem_exists

    def signup_response(self, username, password, c_password):
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

    def on_success_signup(self, username, password, keyfile = False):
        key2 = None
        # Creating all required Directories
        write_remfile(write = True)
        write_remfile('username.txt', username)
        write_AppConfig(keyfile) # writing the configs to run argon2
        password_hash = blake(password) # this is the hash from the password 
        if keyfile:
            key2 = keyfile_encryption(password_hash.encode('utf-8')) # if key file is there then it's generated
        m_key = master_key(key1 = password_hash, key2 = key2, first = True)
        self.create_database(m_key)
        master_key_store(m_key)
        m_key = None
        password_hash = None
        key2 = None
        password = None

    def auth_login(self, master_password, keyfile_dir):
        hash_of_master = blake(master_password)
        if keyfile_dir != None:
            key2 = keyfile_decrypt(hash_of_master.encode('utf-8'), keyfile_dir)
            m_key = master_key(key1=hash_of_master, key2=key2)
            result = auth_hash(m_key)
        else:
            m_key = master_key(key1 = hash_of_master, key2 = None)
            result =  auth_hash(m_key)
        master_password = None
        return [result, m_key]

    def sensitive_data_encrypt(self, sensitive_data):
        random_aes_key = get_random_bytes(32)
        sensitive_data_in_bytes = json.dumps(sensitive_data).encode("utf-8")
        sensitive_data_encrypted = AES_Encrypt(random_aes_key, sensitive_data_in_bytes)
        # assigning random things to sensitive_data
        sensitive_data ={"bs": [1,2,3]}
        return sensitive_data_encrypted, random_aes_key
    
    def create_database(self, masterkey):
        if not checkfile("database.remdb"):
            database = {"Database [main]": [], "Database [main]_categories":{"Default": []}, "$$databases$$": ["Database [main]"]}
            self.encrypt_database(database, masterkey)

    def decrypt_database(self, masterkey):
        encrypt_database = read_remfile("database.remdb")
        encrypt_database = pickle.loads(encrypt_database)
        database_in_bytes = AES_Decrypt(masterkey, encrypt_database) 
        database = json.loads(database_in_bytes)
        masterkey = None
        return database

    def encrypt_database(self, database, masterkey):
        database_in_bytes = json.dumps(database).encode("utf-8")
        encrypted_database = AES_Encrypt(masterkey, database_in_bytes)
        encrypted_database = pickle.dumps(encrypted_database)
        write_remfile("database.remdb", encrypted_database)
        database = {}

    def nat_cmp(self, a, b):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return (alphanum_key(a) > alphanum_key(b)) - (alphanum_key(a) < alphanum_key(b))

    def entry_insertion_index(self, title, database):
        '''
        * here the data base is sent as a list of entries.
        * database must not be empty
        '''
        n = len(database)
        beg = 0
        last = n-1
        import time
        while True:
            mid = (beg+last)//2
            mid_cmp = self.nat_cmp(database[mid]["title"], title)
            if mid != n-1:
                mid_successor_cmp = self.nat_cmp(database[mid+1]["title"], title)
            else:
                mid_successor_cmp = 1
            #print("***")
            #print(mid, mid_cmp, mid_successor_cmp)
            if mid == -1:
                return 0
            elif mid_cmp in (0,-1) and mid_successor_cmp in (0, 1):
                #print("found")
                return mid + 1
            elif mid_cmp == 1: 
                #print("1")
                last = mid - 1  
            elif mid_cmp == -1:
                #print("2")
                beg = mid + 1
            #print("***")

    def add_entry(self, database_name, category, masterkey, entry):
        #decrypt database
        database = self.decrypt_database(masterkey)
        #print("This is the database", database)
        if database[database_name] == []:
            database[database_name].append(entry)
        else:
            #find position for insertion of new element
            insertion_index = self.entry_insertion_index(entry["title"], database[database_name])
            #insert element 
            database[database_name].insert(insertion_index, entry)
            # adding in categories
        category_key = database_name + '_categories'
        if database[category_key][category] == []:
            database[category_key][category].append(entry)
        else:
            insertion_index = self.entry_insertion_index(entry["title"], database[category_key][category])
            database[category_key][category].insert(insertion_index, entry)
        # encrypt the database after adding the entry
        self.encrypt_database(database, masterkey)
        database = None
        masterkey = None

    def add_category(self, database_name, category, masterkey):
        database = self.decrypt_database(masterkey)
        if category in database[database_name+'_categories']:
            database = None
            masterkey = None
            return False
        else:
            database[database_name + '_categories'][category] = []
            self.encrypt_database(database, masterkey)
            database = None
            masterkey = None
            return True
    
    def add_database(self, database_name, masterkey):
        database = self.decrypt_database(masterkey)
        if database_name in database:
            database = None
            masterkey = None
            return False
        else:
            database[database_name] = []
            database[database_name + '_categories'] = {"Default": []}
            database["$$databases$$"].append(database_name)
            self.encrypt_database(database, masterkey)
            database = None
            masterkey = None
            return True

    def return_database_keys(self, masterkey):
        database = self.decrypt_database(masterkey)
        return database["$$databases$$"]

    def return_category_keys(self, database_name, masterkey):
        database = self.decrypt_database(masterkey)
        return list(database[database_name + '_categories'].keys())
    
api = api()
