from FileHandling import *
from EnigmaModule import *
import win32con, win32api, os
import string
from random import randint

Alpha = string.ascii_letters

def MapNumAlpha(n):
	return Alpha[n]

def MapAlphaNum(ch):
	return Alpha.index(ch)


def WriteEncrypt(fileName, paswrd): #This encrypts paswrd and stores passwrd and encryption key in filename. paswrd and key are seperated by sep.
	userkeyFile = open(HomeDir('Data2.txt') , "r")
	listofkeys = ReadFile(userkeyFile)
	userkeyFile.close()
	key = One_Setting_Generator()
	paswrd = EnigmaMachine(paswrd, key)
	keyNo = randint(0,49)
	keyofkey = ''.join(listofkeys[keyNo])
	key = EnigmaMachine(key, keyofkey)
	Nstr = paswrd + key + MapNumAlpha(keyNo)
	file = open(fileName , "a")
	WriteLine(file, Nstr)
	file.close()

def ReadDecrypt(filename): #Reads a file and decrypts it using userkey. Returns list.
	userkeyFile = open(HomeDir('Data2.txt') , "r")
	listofkeys = ReadFile(userkeyFile)
	userkeyFile.close()
	file = open(filename, "r")
	Passwords = ReadFile(file)
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

def SearchFile(Str): #searches for passwords in data3,txt and returns all information of required password. 
	newList = []
	List = ReadDecrypt(HomeDir('Data3.txt'))
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


def Export():
	newList = []
	List = ReadDecrypt(HomeDir('Data3.txt'))
	for ele in List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newList.append(Sublist)
	file = open(Import_Export_Dir('Export File.txt'),'w')
	for ele in newList:
		for sublist in ele:
			file.write(sublist+'&')
		file.write('\n')
	file.close()
#Export()
def Import():
	newList = []
	newListData3 = []
	file = open(Import_Export_Dir('Import File.txt'), 'r')
	List = ReadFile(file)
	del List[len(List)-1]
	for ele in List:
		newList.append(ele.split('&'))
	file.close()
	pass_file = open(HomeDir('Data3.txt'), 'r')
	Data3_List = ReadDecrypt(HomeDir('Data3.txt'))
	for ele in Data3_List:
		Sublist = ele.split('qwertyuiop***asdfghjklzxcvbnm')
		newListData3.append(Sublist)
	pass_file.close()
	file_new = open(HomeDir('Data3.txt'), 'a')
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
				password += subele + 'qwertyuiop***asdfghjklzxcvbnm'
			#print(password)
			WriteEncrypt(HomeDir('Data3.txt'), password)
	file_new.close()

#Import()



