import os
from zipfile import ZipFile
import json
'''-------------------------------------------------------------------------------------'''
app_path = ''
username = 'arjun' # make this empty string later
'''-------------------------------------------------------------------------------------'''

def EOF(file):  # This checks if pointer has reached end of file
    if(file.read() == ''):
        file.seek(0)
        return True
    else:
        return False

def ReadFileLine(file):  # This reads one line from file
    data = file.readline().replace('\n', '')
    return data


def ReadFile(file):  # This reads whole file line by line and returns it as list
    data = file.read().split('\n')
    return data

def WriteLine(file, info):  # Writes line with \n included
    file.writelines(info + '\n')

def set_app_path(path):
    global app_path
    app_path = path + '/'

def set_username(Username):
    global username
    username = Username

def HomeDir(filename, sub_directory = ''): # Appends the subdirectory and filename to the path of the app
    global app_path
    testing = False
    if app_path and not testing:
            print('Here we are!', app_path+sub_directory+'/'+filename)
            return app_path+sub_directory+'/'+filename
    else:
        return sub_directory+'/'+filename

def create_directory(subdirectory): # creates a subdirectory
    try:
        os.makedirs(app_path+subdirectory)
    except:
        pass

def ModifiedFileTime(filepath):
    return os.stat(filepath).st_mtime

#print(ModifiedFileTime( HomeDir('Data2.txt')))


def CheckModified(a, b):
    if a == b:
        return False
    else:
        return True

# Used to write the appconfiguration to the json file
'''WARNING before calling this function all data should be decrypted, new key should be generated to re-encrypt all data'''
def write_AppConfig(time_cost = 2, memory_cost = 51200, parallelism = 8):
    global username
    app_config = json.dumps({"argon2_settings":{"time_cost": time_cost,"memory_cost": memory_cost,"parallelism": parallelism}}, indent=2)
    write_remfile('app_config.json', app_config)


# This opens the .rem file with username as the file name in the UserData directory, here the archive is empty
def write_remfile(filename = '', data = None, write = False, *args): # before sending json data dump it
    global username
    if write: # This is to be made on signup, this initaializes the file
        create_directory('UserData')
        print(HomeDir(username + '.rem'))
        with ZipFile(HomeDir(username + '.rem', 'UserData'), 'w') as rem:
        #with ZipFile('UserData/' + username + '.rem', 'w') as rem: # comment this and use above line for the actual thing
            rem.close()
    else:
        with ZipFile(HomeDir(username + '.rem', 'UserData'), 'a') as rem:
            rem.writestr(filename, data)

def read_remfile(filename):
    global username
    with ZipFile(HomeDir(username + '.rem', 'UserData'), 'r') as rem:
        data = rem.read(filename)
        return data

'''Test the read and write methods'''
def test_read_write():
    write_remfile( write = True)
    #write_remfile('arjun', 'new1.txt', 'hello', write = True)
    write_remfile('new2.json', json.dumps({"hello": 'this is good', "entry":{'username': 'a username' ,'password':'this is a password'}}, indent =2))
    json_data = json.loads(read_remfile('new2.json'))
    print(json_data['entry']['password']) 
    #write_remfile('arjun', 'new1.txt', 'hello2', append = True)

def ReminiscorFiles_Dir(filename):
    homedir = os.path.expanduser('~')
    if os.path.isdir(homedir + '/Reminiscor Files/'):
        newdir = homedir + '/Reminiscor Files/' + filename
    else:
        File_dir = os.path.expanduser('~') 
        direc = "Reminiscor Files"
        os.makedirs(os.path.join(File_dir, direc))
        newdir = homedir + '/Reminiscor Files/' + filename
    return newdir


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
    pfile.seek(0)
    return pfile
