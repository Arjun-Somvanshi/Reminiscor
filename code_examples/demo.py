import json
from random import randint
def random_code(size):
    code = ''
    sample_space = [chr(i) for i in range(65,91)]
    for j in range(48, 58):
        sample_space.append(chr(j))
    for j in range(97, 123):
        sample_space.append(chr(j))
    for i in range (size):
        code+=sample_space[randint(0,len(sample_space)-1)]
    return code
def create_entry():
    entry=[random_code(10),{'username' : random_code(8),'password' : random_code(15),'notes':random_code(30)}]
    return entry
def write_json():
    data= {}
    for i in range(1000):
        e = create_entry()
        data[e[0]] = e[1]
    with open('entry.json', 'w') as f:
        json.dump(data,f, indent = 2, sort_keys=True)

#write_json()  
#DNgrUybs17
def edit(entry, username = 'Arjun', password = 'Arjun1234567890', notes = 'this is a new password to my goole account and everyone can see it' ):
    with open('entry.json') as f:
        data = json.load(f)
    print(data[entry])
    data[entry]['username'] = username
    data[entry]['password'] = password
    data[entry]['notes'] = notes
    print(data[entry])

def delete(entry):
    with open('entry.json') as f:
        data  = json.load(f)
    del data['entry']


#edit('QtqxidIIsS')