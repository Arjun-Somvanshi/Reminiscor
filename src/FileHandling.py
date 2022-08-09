import os
import json
from os.path import dirname, join

'''-------------------------------------------------------------------------------------'''
app_path = ''
external_path = ''
username = '' # make this empty string later
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

def set_app_path(platform, app_name, portable = False, path = ""):
    global app_path, external_path
    if portable and platform!= 'android':
        app_path = path 
    else:
        print("The platform is: ", platform)
        if platform == 'win':
            app_path = os.getenv('APPDATA') + os.path.sep + app_name
        elif platform == 'linux':
            app_path = os.path.expanduser('~') + os.path.sep + "."+app_name.lower()
        elif platform == 'macosx':
            app_path = os.path.expanduser('~/Library/Application Support/{}'.format(app_name))
        elif platform == 'android':
            from android.storage import app_storage_path, primary_external_storage_path
            app_path = app_storage_path()
            external_path = primary_external_storage_path()
    app_path += os.path.sep
    return app_path, external_path

def HomeDir(filename, sub_directory = ''): # Appends the subdirectory and filename to the path of the app
    global app_path
    testing = False
    if app_path and not testing:
            return app_path+sub_directory+'/'+filename
            print("HomeDir is: ", sub_directory+'/'+filename)
    else:
        print("HomeDir is: ", sub_directory+'/'+filename)
        return sub_directory+'/'+filename

def create_directory(subdirectory): # creates a subdirectory
    try:
        os.makedirs(app_path+subdirectory)
    except:
        pass

def return_username():
    with open(HomeDir('username.txt', 'UserData'), 'r') as f:
        return f.read()

# Used to write the appconfiguration to the json file
'''WARNING before calling this function all data should be decrypted, new key should be generated to re-encrypt all data'''
def write_AppConfig(keyfile, time_cost = 2, memory_cost = 51200, parallelism = 8):
    global username
    app_config = {"argon2_settings":{"time_cost": time_cost,"memory_cost": memory_cost,"parallelism": parallelism}}
    if keyfile:
        app_config['KeyFile'] = True
        write_remfile('app_config.json', app_config)
    else:    
        write_remfile('app_config.json', app_config)


# This opens the .rem file with username as the file name in the UserData directory, here the archive is empty
def write_remfile(filename = '', data = None, write = False, *args): # before sending json data dump it
    '''To write in the rem file (reminiscor archive). filename, name of the file you want to write (no appends), data is 
    the content you want to write, write is only to be used when using this function for the first time (during signup)'''
    if write: # This is to be made on signup, this initaializes the file
        create_directory('UserData')
        create_directory('UserData'+os.path.sep+'Databases')
    else:
        file_type = filename.split('.')[1]
        if file_type =='json':
            with open(HomeDir(filename, 'UserData'), 'w') as f:
                json.dump(data,f,indent =2)
        elif file_type == 'bin' or file_type == 'dat' or file_type == 'remdb':
            with open(HomeDir(filename, 'UserData'), 'wb') as f:
                f.write(data)
        elif file_type == 'txt':
            with open(HomeDir(filename, 'UserData'), 'w') as f:
                f.write(data)

def read_remfile(filename):
    '''read all the data from a particular file in the .rem archive'''
    file_type = filename.split('.')[1]
    if file_type =='json':
        with open(HomeDir(filename, 'UserData'), 'r') as f:
            data = json.load(f)
            print("this is hte data from read_remfile ", data)
    elif file_type == 'bin' or file_type == 'dat' or file_type == 'remdb':
        with open(HomeDir(filename, 'UserData'), 'rb') as f:
            data = f.read()
    elif file_type == 'txt':
        with open(HomeDir(filename, 'UserData'), 'r') as f:
            data = f.read()
    return data

def checkfile(filename):
    return os.path.isfile(HomeDir(filename, 'UserData'))
'''Test the read and write methods'''
def test_read_write():
    write_remfile( write = True)
    #write_remfile('arjun', 'new1.txt', 'hello', write = True)
    write_remfile('new2.json', json.dumps({"hello": 'this is good', "entry":{'username': 'a username' ,'password':'this is a password'}}, indent =2))
    json_data = json.loads(read_remfile('new2.json'))
    print(json_data['entry']['password']) 
    #write_remfile('arjun', 'new1.txt', 'hello2', append = True)

'''app_config = json.loads(read_remfile('app_config.json'))
app_config["This will work"] = True
write_remfile('app_config.json', json.dumps(app_config))'''
