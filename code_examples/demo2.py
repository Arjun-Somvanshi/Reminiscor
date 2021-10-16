from demo import create_entry
from security import *
data = {}
def create_test_database():
    for i in range(1000):
        e = create_entry()
        data[e[0]] = e[1]
        plain_text = json.dumps(data).encode('utf-8')
        key = b'E\x82b\x7f\x969\xf4\x81\xf5\x8e\xb6\xcf\xf6?nS\xf2\x99# a\xde\xaa#\x7f6\xa4aBDpY'
        encrypted_data = AES_Encrypt(key, plain_text)
        with open('database.json', 'w') as f:
            json.dump(encrypted_data,f,indent=2)
def read():
    with open('database.json') as f:
        cipher_data = json.load(f)
        print(cipher_data['iv'], '\n',cipher_data['ct'])
#create_test_database()