import os.path
from Password_Read_Write import *
from FileHandling import *
def CheckUser():
	if os.path.isfile(HomeDir('Data1.dat')):
		return True
	else:
		return False
def CheckCredentials(usrName, paswrd, key):
	try:
		Credentials_Data=ReadDecrypt(HomeDir('Data1.dat'),key)
	except:
		print('a')
		return False
	else:
		cred_string=''.join(Credentials_Data[0])
		Credentials=cred_string.split('qwertyuiop***asdfghjklzxcvbnm')
		if Credentials[0] == usrName and Credentials[1] == paswrd:
			print('b')
			return True
		else:
			print(Credentials)
			print('c')
			return False



