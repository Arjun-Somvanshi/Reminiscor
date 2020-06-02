# Module to handle Enigma Level Encryption 
from random import randint, shuffle
import string 
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

	
def Default_Unique_User_EnigmaSettings():
	user_keys=[]
	for i in range(0,50):
		user_keys.append(One_Setting_Generator())
	file=open(HomeDir('Data2.txt'),'w')
	for i in user_keys:
		WriteLine(file,i)
	file.close()
	#HideFile(HomeDir('Data2.txt'))#Default_Unique_User_EnigmaSettings()

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




	
