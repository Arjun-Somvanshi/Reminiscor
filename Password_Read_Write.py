from FileHandling import *
from EnigmaModule import *
import string
from random import randint
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import pbkdf2
import pyaes
Alpha = string.ascii_letters

def MapNumAlpha(n):
	return Alpha[n]

def MapAlphaNum(ch):
	return Alpha.index(ch)


def WriteEncrypt(fileName, paswrd,master_password): #This encrypts paswrd and stores passwrd and encryption key in filename. paswrd and key are seperated by sep.
	userkeyFile = open(HomeDir('Data2.txt') , "r")
	listofkeys1 = ReadFile(userkeyFile)
	listofkeys=[]
	for i in listofkeys1:
		key = pbkdf2.crypt(master_password)
		key_32 = key[:32]
		key_32_bytes=str.encode(key_32)
		iv = "InitializationVe"
		aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
		decrypted = aes.decrypt(i)
		a=str(decrypted)
		listofkeys.append(a)
	userkeyFile.close()
	key = One_Setting_Generator()
	paswrd = EnigmaMachine(paswrd, key)
	keyNo = randint(0,49)
	keyofkey = ''.join(listofkeys[keyNo])
	key = EnigmaMachine(key, keyofkey)
	Nstr = paswrd + key + MapNumAlpha(keyNo)
	key = pbkdf2.crypt(master_password)
	key_32 = key[:32]
	key_32_bytes=str.encode(key_32)
	iv = "InitializationVe"
	aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
	ciphertext = aes.encrypt(Nstr)
	file = open(fileName , "a")
	WriteLine(file, str(ciphertext))
	file.close()

def ReadDecrypt(filename, master_password): #Reads a file and decrypts it using userkey. Returns list.
	userkeyFile = open(HomeDir('Data2.txt') , "r")
	listofkeys1 = ReadFile(userkeyFile)
	listofkeys=[]
	for i in listofkeys1:
		key = pbkdf2.crypt(master_password)
		key_32 = key[:32]
		key_32_bytes=str.encode(key_32)
		iv = "InitializationVe"
		aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
		decrypted = aes.decrypt(i)
		a=str(decrypted,'utf-8')
		listofkeys.append(a)
	userkeyFile.close()
	file = open(filename, "r")
	Passwords1 = ReadFile(file)
	Passwords=[]
	for i in Passwords1:
		key = pbkdf2.crypt(master_password)
		key_32 = key[:32]
		key_32_bytes=str.encode(key_32)
		iv = "InitializationVe"
		aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
		decrypted = aes.decrypt(i)
		a=str(decrypted,'utf-8')
		Passwords.append(a)
	file.close()
	Passwords.pop()
	decp = []
	for p in Passwords:
		KeyAlpha = p[-1:]
		keyNo = MapAlphaNum(KeyAlpha)
		UserKey = listofkeys[keyNo]
		randKeyIndex = len(p)-655
		key = p[randKeyIndex:len(p)-1]
		deckey = EnigmaMachine(key, UserKey)
		decp.append(EnigmaMachine(p[0:randKeyIndex],deckey))
	return decp

def SearchFile(Str,master_password): #searches for passwords in data3,txt and returns all information of required password. 
	newList = []
	List = ReadDecrypt(HomeDir('Data3.txt'),master_password)
	ind=None
	for ele in List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newList.append(Sublist)
	for sublist in newList:
		if sublist[0].lower() == Str.lower():
			ind = newList.index(sublist)
			break
		else:
			ind = None
	if ind == None:
		return []
	else:
		return newList[ind]


def Export(master_password):
	List = ReadDecrypt(HomeDir('Data3.txt'),master_password)
	if os.path.isfile(Import_Export_Dir('Password File.txt')):
		os.chmod(Import_Export_Dir('Password File.txt'), S_IWUSR|S_IREAD)
	temp = open(Import_Export_Dir('Password File.txt'), 'w')
	temp = deleteContent(temp)
	temp.close()
	file = open(Import_Export_Dir('Password File.txt'),'w')
	for ele in List:
		if List.index(ele) == len(List) - 1:
			file.write(ele)
		else:
			file.write(ele + '\n')
	os.chmod(Import_Export_Dir('Password File.txt'), S_IREAD|S_IRGRP|S_IROTH)
	file.close()
#Export()
def Import(master_password):
	newList = []
	newListData3 = []
	if os.path.isfile(Import_Export_Dir('Password File.txt')) and os.stat(Import_Export_Dir('Password File.txt')).st_size is not 0:
		file = open(Import_Export_Dir('Password File.txt'), 'r')
		List = ReadFile(file)
		for ele in List:
			newList.append(ele.split('qwertyuiop***asdfghjklzxcvbnm'))
		file.close()
		pass_file = open(HomeDir('Data3.txt'), 'r')
		Data3_List = ReadDecrypt(HomeDir('Data3.txt'),master_password)
		for ele in Data3_List:
			Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
			newListData3.append(Sublist)
		pass_file.close()
		file_new = open(HomeDir('Data3.txt'), 'a')
		temp = False
		for ele1 in newList:
			for ele2 in newListData3:
				if ele1[0].lower() == ele2[0].lower():
					temp = True
					break
				else:
					temp = False
			if temp == False:
				password = ''
				for subele in ele1:
					if not ele1.index(subele) == len(ele1)-1: 
						password += subele + 'qwertyuiop***asdfghjklzxcvbnm'
					else:
						password += subele
				WriteEncrypt(HomeDir('Data3.txt'), master_password)
		os.chmod(Import_Export_Dir('Password File.txt'), S_IWUSR|S_IREAD)
		temp1=open(Import_Export_Dir("Password File.txt"),'w')
		temp1=deleteContent(temp1)
		temp1.close()
		file_new.close()
		
		return True
	else:
		return False
#Import()

def DelPassword(entry,master_password):
	newListData3 = []
	pass_file = open(HomeDir('Data3.txt'), 'r')
	Data3_List = ReadDecrypt(HomeDir('Data3.txt'),master_password)
	for ele in Data3_List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newListData3.append(Sublist)
	pass_file.close()
	if entry in newListData3:
		newListData3.remove(entry)
		temp = open(HomeDir('Data3.txt'), 'w')
		temp = deleteContent(temp)
		temp.close()
		for passList in newListData3:
			passwrd = ''
			a=0
			for ele in passList:
				if a == len(passList)-1:
					passwrd += ele 
					a+=1
				else:
					passwrd += ele + 'qwertyuiop***asdfghjklzxcvbnm'
					a+=1
			WriteEncrypt(HomeDir('Data3.txt'), master_passwrd)
	else:
		pass


def EditPassword(iniEntry, entry,master_password): #replaces iniEntry with entry
	newListData3 = []
	pass_file = open(HomeDir('Data3.txt'), 'r')
	Data3_List = ReadDecrypt(HomeDir('Data3.txt'),master_password)
	for ele in Data3_List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newListData3.append(Sublist)
	pass_file.close()
	if iniEntry in newListData3: 
		index = newListData3.index(iniEntry)
		newListData3.remove(iniEntry)
		if CheckFunction(entry, newListData3):
			return True
		else:
			newListData3.insert(index, entry)
			temp = open(HomeDir('Data3.txt'), 'w')
			temp = deleteContent(temp)
			temp.close()
			for passList in newListData3:
				passwrd = ''
				a=0
				for ele in passList:
					if not a == len(passList)-1:
						passwrd += ele + 'qwertyuiop***asdfghjklzxcvbnm'
						a+=1
					else:
						passwrd += ele
						a+=1
				WriteEncrypt(HomeDir('Data3.txt'), master_passwrd)
			return False
	else:
		pass

def CheckFunction(List, LOL):
	for element in LOL:
		if List[0] == element[0]:
			return True
	return False
#print(ReadDecrypt(HomeDir('Data3.txt')))