import pyaes
import pbkdf2
from EnigmaModule import *
#Creating AES key and encrypting enigma setting 
salt = b'\x05;iBi\x17Q\xe0'
key_32_bytes = pbkdf2.PBKDF2("Arjun2000@!", salt).read(32)
aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
enigmakey = One_Setting_Generator()
enigmakey1 = One_Setting_Generator()
txt=enigmakey+'\n'+enigmakey1
ciphertext = aes.encrypt(txt)
print(txt+'\n\n')
#Writing encrypted enigma setting in file
file = open("Newfile.dat", "bw")
file.write(ciphertext)
file.close()
#new key
master_password=input("Enter password: ")
key1_32_bytes = pbkdf2.PBKDF2(master_password, salt).read(32)
#Reading from file and decypting
file1 =open("Newfile.dat", "br")
something = file1.read()
aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
decrypted = aes.decrypt(something)
#using a wrong key to decrypt
print(key_32_bytes)
print('\n\n\n')
print(key1_32_bytes)
print('\n\n\n')
try:
	aes = pyaes.AESModeOfOperationCTR(key1_32_bytes)
	decrypted = aes.decrypt(something)
	a=str(decrypted, 'utf-8')
	l=a.split('\n')
	print(l)
except:
	print('wrong key')
	file1.close()
else:
	print('right key!')
	file1.close()

a=input()