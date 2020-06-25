from FileHandling import *
from EnigmaModule import *
import pyaes
import pbkdf2
import string
from random import randint
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

Alpha = string.ascii_letters

def MapNumAlpha(n):
	return Alpha[n]

def MapAlphaNum(ch):
	return Alpha.index(ch)


def WriteEncrypt(fileName, message, AESkey): #This encrypts paswrd and stores passwrd and encryption key in filename. paswrd and key are seperated by sep.
	
	#Get list all user keys
	userkeyFile = open(HomeDir('Data2.dat') , "br")
	Allkeys = userkeyFile.read()
	userkeyFile.close()
	
	#Decrypt AES encryption
	aes = pyaes.AESModeOfOperationCTR(AESkey)
	decryptedUserKeys = aes.decrypt(Allkeys)

	#Break decrypted user key file into list 
	UserKeyList = str(decryptedUserKeys, 'utf-8').split('\n')

	#Create a new key, enigma encrypt the password and enigma encrypt the key using a random key from List 
	key = One_Setting_Generator()
	EncryptedMessage = EnigmaMachine(message, key)
	keyNo = randint(0,49)
	keyofkey = ''.join(UserKeyList[keyNo])
	key = EnigmaMachine(key, keyofkey)
	Nstr = EncryptedMessage + key + MapNumAlpha(keyNo)
	
	#Read filename and decrypt it
	fread = open(fileName, "br")
	filedata = fread.read() 
	fread.close()
	aes = pyaes.AESModeOfOperationCTR(AESkey)
	decryptedfiledata = str(aes.decrypt(filedata), 'utf-8')

	#Append Nstr in filedata
	if decryptedfiledata == '':
		decryptedfiledata += Nstr
	else:
		decryptedfiledata += '\n' + Nstr
	#AES encrypt Nstr
	print(decryptedfiledata)
	aes = pyaes.AESModeOfOperationCTR(AESkey)
	Encryptedfiledata = aes.encrypt(decryptedfiledata)

	#Store key in file with name FileName
	file = open(fileName , "bw")
	file = deleteContent(file)
	file.write(Encryptedfiledata)
	file.close()

'''
salt = b'\x05;iBi\x17Q\xe0'
key_32_bytes = pbkdf2.PBKDF2("Arjun2000@!", salt).read(32)
#Default_Unique_User_EnigmaSettings(key_32_bytes)
WriteEncrypt(HomeDir('Data3.dat'), 'Githubqwertyuiop***asdfghjklzxcvbnmmanusomvanshi@hotmail.comqwertyuiop***asdfghjklzxcvbnmmanu2002qwertyuiop***asdfghjklzxcvbnm something', key_32_bytes)
'''
def ReadDecrypt(filename, AESkey): #Reads a file and decrypts it using userkey. Returns list.
	#Read all user keys from Data2.dat
	userkeyFile = open(HomeDir('Data2.dat') , "br")
	Allkeys = userkeyFile.read()
	userkeyFile.close()
	
	#Open filename and read all data from it 
	file = open(filename, "br")
	FileData = file.read()
	file.close()

	#AES decrypt both files
	aes = pyaes.AESModeOfOperationCTR(AESkey)
	decryptedUserKeys = aes.decrypt(Allkeys)
	aes = pyaes.AESModeOfOperationCTR(AESkey)
	decryptedFileData = aes.decrypt(FileData)
	print(decryptedFileData)
	#Create Lists for both files
	UserKeyList = str(decryptedUserKeys, 'utf-8').split('\n')
	FileDataList = str(decryptedFileData, 'utf-8').split('\n')

	#Decrypt using Enigma key 
	decp = []
	if not (FileDataList ==['']):
		for p in FileDataList:
			KeyAlpha = p[-1:]
			keyNo = MapAlphaNum(KeyAlpha)
			UserKey = UserKeyList[keyNo]
			randKeyIndex = len(p)-655
			key = p[randKeyIndex:len(p)-1]
			deckey = EnigmaMachine(key, UserKey)
			decp.append(EnigmaMachine(p[0:randKeyIndex],deckey))
	return decp
'''
salt = b'\x05;iBi\x17Q\xe0'
key_32_bytes = pbkdf2.PBKDF2("Arjun2000@!", salt).read(32)
print(ReadDecrypt(HomeDir('Data3.dat'), key_32_bytes))
'''
def SearchFile(Str, AESkey): #searches for passwords in data3 and returns all information of required password. 
	newList = []
	List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
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


def Export(AESkey):
	List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
	if os.path.isfile(Import_Export_Dir('Password File.dat')):
		os.chmod(Import_Export_Dir('Password File.dat'), S_IWUSR|S_IREAD)
	temp = open(Import_Export_Dir('Password File.dat'), 'bw')
	temp = deleteContent(temp)
	temp.close()
	file = open(Import_Export_Dir('Password File.dat'),'bw')
	for ele in List:
		if List.index(ele) == len(List) - 1:
			file.write(ele)
		else:
			file.write(ele + '\n')
	os.chmod(Import_Export_Dir('Password File.dat'), S_IREAD|S_IRGRP|S_IROTH)
	file.close()
#Export()
def Import(AESkey):
	newList = []
	newListData3 = []
	if os.path.isfile(Import_Export_Dir('Password File.dat')) and os.stat(Import_Export_Dir('Password File.dat')).st_size is not 0:
		file = open(Import_Export_Dir('Password File.dat'), 'br')
		List = ReadFile(file)
		for ele in List:
			newList.append(ele.split('qwertyuiop***asdfghjklzxcvbnm'))
		file.close()
		pass_file = open(HomeDir('Data3.dat'), 'br')
		Data3_List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
		for ele in Data3_List:
			Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
			newListData3.append(Sublist)
		pass_file.close()
		file_new = open(HomeDir('Data3.dat'), 'ba')
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
				WriteEncrypt(HomeDir('Data3.dat'), password, AESkey)
		os.chmod(Import_Export_Dir('Password File.dat'), S_IWUSR|S_IREAD)
		temp1=open(Import_Export_Dir("Password File.dat"),'w')
		temp1=deleteContent(temp1)
		temp1.close()
		file_new.close()
		
		return True
	else:
		return False
#Import()

def DelPassword(entry,AESkey):
	newListData3 = []
	Data3_List = ReadDecrypt(HomeDir('Data3.dat'),AESkey)
	for ele in Data3_List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newListData3.append(Sublist)
	if entry in newListData3:
		newListData3.remove(entry)
		temp = open(HomeDir('Data3.dat'), 'bw')
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
			WriteEncrypt(HomeDir('Data3.dat'), passwrd, AESkey)
	else:
		pass


def EditPassword(iniEntry, entry, AESkey): #replaces iniEntry with entry
	newListData3 = []
	pass_file = open(HomeDir('Data3.dat'), 'r')
	Data3_List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
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
			temp = open(HomeDir('Data3.dat'), 'w')
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
				WriteEncrypt(HomeDir('Data3.dat'), passwrd, AESkey)
			return False
	else:
		pass

def CheckFunction(List, LOL):
	for element in LOL:
		if List[0] == element[0]:
			return True
	return False
#print(ReadDecrypt(HomeDir('Data3.dat')))