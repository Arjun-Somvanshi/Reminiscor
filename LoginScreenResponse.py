import os.path
from Password_Read_Write import *
from FileHandling import *
def CheckUser():
	if os.path.isfile(HomeDir('Data1.txt')):
		return True
	else:
		return False
def CheckCredentials(usrName, paswrd):
	try:
		Credentials_Data=ReadDecrypt(HomeDir('Data1.txt'),paswrd)
	except:
		return False
	else:
		cred_string=''.join(Credentials_Data[0])
		Credentials=cred_string.split('qwertyuiop***asdfghjklzxcvbnm')
		if Credentials[0] == usrName and Credentials[1] == paswrd:
			return True
		else:
			return False



