import pyaes
import pbkdf2
from EnigmaModule import *
#Creating AES key and encrypting enigma setting 
password='manvendra2'
key=pbkdf2.crypt(password)
key_32 = key[:32]
key_32_bytes=str.encode(key_32)
aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
enigmakey = One_Setting_Generator()
ciphertext = aes.encrypt(enigmakey)

#Writing encrypted enigma setting in file
file = open("Newfile.dat", "bw")
file.write(ciphertext)
file.close()
#new key
password1='manvendra'
key1=pbkdf2.crypt(password1)
key1_32 = key1[:32]
key1_32_bytes=str.encode(key1_32)
print(key1_32_bytes)
#Reading from file and decypting
file1 =open("Newfile.dat", "br")
something = file1.read()
aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
decrypted = aes.decrypt(something)
print(str(decrypted, 'utf-8'))
#using a wrong key to decrypt
try:
	aes = pyaes.AESModeOfOperationCTR(key1_32_bytes)
	decrypted = aes.decrypt(something)
	print(str(decrypted, 'utf-8'))
except:
	print('wrong key')
	file1.close()
else:
	print('right key!')
	file1.close()

