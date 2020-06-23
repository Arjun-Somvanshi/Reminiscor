import pbkdf2
import pyaes
from FileHandling import*
from EnigmaModule import*
file = open(HomeDir('Data2.txt'), "w")
password = "manvendra2"
key = pbkdf2.crypt(password)
key_32 = key[:32]
key_32_bytes=str.encode(key_32)
iv = "InitializationVe"
aes = pyaes.AESModeOfOperationCTR(key_32_bytes)
enigmakey = One_Setting_Generator()
ciphertext = aes.encrypt(enigmakey)
file.write(str(ciphertext))
file.close()
file1 = open(HomeDir('Data2.dat'), "br")
List = ReadFile(file1)
for i in List:
	i=str.encode(i)
list1=[]
for i in List:
	decrypted = aes.decrypt(i)
	a=str(decrypted)
	list1.append(a)
print(list1)
file1.close()

