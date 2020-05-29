import win32api, win32con, os, os.path
def EOF(file): #This checks if pointer has reached end of file
	if(file.read() == ''):
		file.seek(0)
		return True
	else:
		return False

def ReadFileLine(file): #This reads one line from file
	data = file.readline().replace('\n', '')
	return data

def ReadFile(file): #This reads whole file line by line and returns it as list
	data = file.read().split('\n')
	return data

def WriteSeperator(file, info, sep): #This writes each element of list inot a file where the elements are sperated by sep
	infoStr= ''
	for char in info:
		infoStr = infoStr + char + sep
	file.write(infoStr+'\n')

def ReadSeperator(file, sep): #Reads file and seperates string using sep, returns list
	data = ReadFileLine(file)
	data.split(sep)
	return data

def WriteLine(file, info): #Writes line with \n included
	file.writelines(info + '\n')

def HideFile(fileName): #Hides file
	win32api.SetFileAttributes(fileName, win32con.FILE_ATTRIBUTE_HIDDEN)

def HomeDir(filename):
	homedir = os.path.expanduser('~')
	newdir = homedir + '\\AppData\\Roaming\\Reminiscor\\'+filename
	return newdir

def ModifiedFileTime(filepath):
	return os.stat(filepath).st_mtime

#print(ModifiedFileTime( HomeDir('Data2.txt')))

def CheckModified(a , b):
	if a == b:
		return False
	else:
		return True

def Import_Export_Dir(filename):
	homedir = os.path.expanduser('~')
	if os.path.isdir(homedir + '\\Documents\\Reminiscor Export_Import\\'):	
		newdir = homedir + '\\Documents\\Reminiscor Export_Import\\'+ filename
	else:
		File_dir = os.path.expanduser('~') + '\\Documents'
		direc = "Reminiscor Export_Import"
		os.mkdir(os.path.join(File_dir, direc))
		newdir = homedir + '\\Documents\\Reminiscor Export_Import\\'+ filename
	return newdir