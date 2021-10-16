from zipfile import ZipFile
import pickle

database = {'entries':{'username': 'arjun somvanshi', 'password': 'arjun2000123455667'}}
data = pickle.dumps(database)
# Now the data will be encrypted
with open('database.reminiscor', 'wb') as dbfile:
    dbfile.write(data)

with open('database.reminiscor', 'rb') as dbfile:
    data = dbfile.read()

database = pickle.loads(data)

print(database)