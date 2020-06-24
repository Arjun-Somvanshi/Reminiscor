# Module to handle Enigma Level Encryption 
from random import randint, shuffle
import string 
import pbkdf2
import pyaes
from FileHandling import *
def One_Setting_Generator(): #Generates one enigma setting with 'qwertyuiop***asdfghjklzxcvbnm' as a seperator

#    PLUGBOARD IS DIFFERENT EACH LETTER IS MUTUALLY MATCHED
	p=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f')
	shuffle(p)
	p1=[]
	p2=[]
	for i in range(0,48):
		p1.append(p[i])
	for i in range (48,96):
		p2.append(p[i])
	plugboard=[p1,p2]	
#   REFLECTOR IS ALSO DIFFERENT EACH LETTER IS MUTUALLY MATCHED 
	r=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f')
	shuffle(r)
	r1=[]
	r2=[]
	for i in range(0,48):
		r1.append(r[i])
	for i in range (48,96):
		r2.append(r[i])
	reflector=[r1,r2]

	rotor1=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f')
	rotor2=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f')
	rotor3=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f')
	shuffle(rotor1)
	shuffle(rotor2)
	shuffle(rotor3)
	sep=list('qwertyuiop***asdfghjklzxcvbnm')
	setting=plugboard[0]+sep+plugboard[1]+sep+rotor1+sep+rotor2+sep+rotor3+sep+reflector[0]+sep+reflector[1]
	return ''.join(setting)

def KeyDerivationFunction(master_password,skey):
	key=skey.split('qwertyuiop***asdfghjklzxcvbnm')
	pl1=''
	pl2=''
	rf1=''
	rf2=''
	for i in master_password:
		if i in key[0]:
			key[0].replace(i,'')
			key[5].replace(i,'')
			pl1+=i
			rf1+=i
		elif i in key[1]:
			key[1].replace(i,'')
			key[6].replace(i,'')
			pl2+=i
			rf2+=i
	key[0]+=pl1
	key[1]+=pl2
	key[5]+=rf1
	key[6]+=rf2
	for i in master_password:
		key[2].replace(i,'')
		key[3].replace(i,'')
		key[4].replace(i,'')
	key[2]+=master_password
	key[3]+=master_password
	key[4]+=master_password
	sep='******'
	derivedkey=''
	derivedkey+=key[0]+sep+key[1]+sep+key[2]+sep+key[3]+sep+key[4]+sep+key[5]+sep+key[6]
	#print(derivedkey)
#KeyDerivationFunction('Arjun2000',One_Setting_Generator())
def Default_Unique_User_EnigmaSettings(master_password):
	user_keys=[]
	for i in range(0,50):
		if i==49:
			user_keys.append(One_Setting_Generator())####To SEPERATE SETTINGS BEFORE WRITIN EM INTO DATA 2
		else:
			user_keys.append(One_Setting_Generator()+'\n')

	file=open(HomeDir('Data2.dat'),'bw')
	aes = pyaes.AESModeOfOperationCTR(master_password)
	ciphertext = aes.encrypt(''.join(user_keys))
	file.write(ciphertext)
	file.close()

def EnigmaMachine(msg_str,enigma_setting_str):
	enigma=enigma_setting_str.split('qwertyuiop***asdfghjklzxcvbnm') #stores the five rotors as strings in a list
	plugboard=[]
	reflector=[]
	plugboard.append(list(enigma[0]))
	plugboard.append(list(enigma[1]))
	rotor1=list(enigma[2])
	rotor2=list(enigma[3])
	rotor3=list(enigma[4])
	reflector.append(list(enigma[5]))
	reflector.append(list(enigma[6]))
	Ordered_List=list(string.punctuation+string.ascii_letters+string.digits+' '+'\x1f') #A list with correct arrangement of characters
	t_plugboard=plugboard[0]+plugboard[1]
	t_reflector=reflector[0]+reflector[1]
	message=list(msg_str)
	Encrypted_Msg=''
	def move_rotor(rotor):
		first_char=rotor[0]
		for i in range(0,len(rotor)-1):
			rotor[i]=rotor[i+1]
		rotor[len(rotor)-1]=first_char
		return rotor
	for char in message:
		rotor1_firstchar=rotor1[0]
		rotor2_firstchar=rotor2[0]
		#PlugBoard Character is mapped to orignal message charachter
		i=t_plugboard.index(char)
		if i<=47:
			char=plugboard[1][i]
		else:
			char=plugboard[0][i-48]
		#Rotor1 Character is mapped to PlugBoard charachter
		i=Ordered_List.index(char)
		char=rotor1[i]
		#Rotor2 Character is mapped to Rotor1 charachter
		i=Ordered_List.index(char)
		char=rotor2[i]
		#Rotor3 Character is mapped to Rotor2 charachter
		i=Ordered_List.index(char)
		char=rotor3[i]
		#Reflector Character is mapped to Rotor3 charachter
		i=t_reflector.index(char)
		if i<=47:
			char=reflector[1][i]
		else:
			char=reflector[0][i-48]
		#Reflector sends signal back to rotor 3
		#Rotor3 Character is mapped to Reflector charachter
		i=rotor3.index(char)
		char=Ordered_List[i]
		#Rotor2 Character is mapped to Rotor3 charachter
		i=rotor2.index(char)
		char=Ordered_List[i]
		#Rotor1 Character is mapped to Rotor2 charachter
		i=rotor1.index(char)
		char=Ordered_List[i]
		#PlugBoard Character is mapped to Rotor2 charachter
		i=t_plugboard.index(char)
		if i<=47:
			char=plugboard[1][i]
		else:
			char=plugboard[0][i-48]
		Encrypted_Msg+=char
		rotor1= move_rotor(rotor1)
		if rotor1_firstchar==rotor1[0]:
			rotor2= move_rotor(rotor2)
		if rotor2_firstchar==rotor2[0]:
			rotor3= move_rotor(rotor3)
	return Encrypted_Msg	

#Module ends anything beneath is for testing the module 
def createuser():
	Default_Unique_User_EnigmaSettings()
def testmodule():
	s= One_Setting_Generator()
	m='Einstein describled space time as a four dimensional pseudo riemanian manifold. All free falling paths in space time are described by "geodesic equations"'
	file=open("test.txt",'w')
	em=EnigmaMachine(m,s)
	WriteLine(file,em)
	file.close()
	file1=open('test.txt','r')
	dm=ReadFileLine(file1)
	file1.close()
	dm=EnigmaMachine(dm,s)
	print(dm)
#createuser()
#testmodule()
#o=One_Setting_Generator()
#print(len(o))
#p=o.split('qwertyuiop***asdfghjklzxcvbnm')
#print(len(p[0]),'\n',len(p[1]),'\n',len(p[2]))




	
