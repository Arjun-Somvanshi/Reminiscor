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

#WriteEncrypt("Passwords.txt", "Manu2002")
def ReadDecrypt(filename):
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

#print(ReadDecrypt(HomeDir('Data3.txt')))







