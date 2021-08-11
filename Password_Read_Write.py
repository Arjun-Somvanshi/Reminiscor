from FileHandling import *
from EnigmaModule import *
import pyaes
import pbkdf2
import string
from random import randint
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import os
Alpha = string.ascii_letters


def MapNumAlpha(n):
    return Alpha[n]


def MapAlphaNum(ch):
    return Alpha.index(ch)


# This encrypts paswrd and stores passwrd and encryption key in filename. paswrd and key are seperated by sep.
def WriteEncrypt(fileName, message, AESkey):

    # Get list all user keys
    userkeyFile = open(HomeDir('Data2.dat'), "br")
    Allkeys = userkeyFile.read()
    userkeyFile.close()

    # Decrypt AES encryption
    aes = pyaes.AESModeOfOperationCTR(AESkey)
    decryptedUserKeys = aes.decrypt(Allkeys)

    # Break decrypted user key file into list
    UserKeyList = str(decryptedUserKeys, 'utf-8').split('\n')

    # Create a new key, enigma encrypt the password and enigma encrypt the key using a random key from List
    key = One_Setting_Generator()
    EncryptedMessage = EnigmaMachine(message, key)
    keyNo = randint(0, 49)
    keyofkey = ''.join(UserKeyList[keyNo])
    key = EnigmaMachine(key, keyofkey)
    Nstr = EncryptedMessage + key + MapNumAlpha(keyNo)

    # Read filename and decrypt it
    fread = open(fileName, "br")
    filedata = fread.read()
    fread.close()
    aes = pyaes.AESModeOfOperationCTR(AESkey)
    decryptedfiledata = str(aes.decrypt(filedata), 'utf-8')

    # Append Nstr in filedata
    if decryptedfiledata == '':
        decryptedfiledata += Nstr
    else:
        decryptedfiledata += '\n' + Nstr

    # AES encrypt Nstr
    aes = pyaes.AESModeOfOperationCTR(AESkey)
    Encryptedfiledata = aes.encrypt(decryptedfiledata)

    # Store key in file with name FileName
    file = open(fileName, "bw")
    file = deleteContent(file)
    file.write(Encryptedfiledata)
    file.close()


'''
salt = b'\x05;iBi\x17Q\xe0'
key_32_bytes = pbkdf2.PBKDF2("Arjun2000@!", salt).read(32)
#Default_Unique_User_EnigmaSettings(key_32_bytes)
WriteEncrypt(HomeDir('Data3.dat'), 'Netflixqwertyuiop***asdfghjklzxcvbnmmanusomvanshi@hotmail.comqwertyuiop***asdfghjklzxcvbnmmanu2002qwertyuiop***asdfghjklzxcvbnm something', key_32_bytes)
'''


# Reads a file and decrypts it using userkey. Returns list.
def ReadDecrypt(filename, AESkey):
    # Read all user keys from Data2.dat
    userkeyFile = open(HomeDir('Data2.dat'), "br")
    Allkeys = userkeyFile.read()
    userkeyFile.close()

    # Open filename and read all data from it
    file = open(filename, "br")
    FileData = file.read()
    file.close()

    # AES decrypt both files
    aes = pyaes.AESModeOfOperationCTR(AESkey)
    decryptedUserKeys = aes.decrypt(Allkeys)
    aes = pyaes.AESModeOfOperationCTR(AESkey)
    decryptedFileData = aes.decrypt(FileData)
    # Create Lists for both files
    UserKeyList = str(decryptedUserKeys, 'utf-8').split('\n')
    FileDataList = str(decryptedFileData, 'utf-8').split('\n')

    # Decrypt using Enigma key
    decp = []
    if not (FileDataList == ['']):
        for p in FileDataList:
            KeyAlpha = p[-1:]
            keyNo = MapAlphaNum(KeyAlpha)
            UserKey = UserKeyList[keyNo]
            randKeyIndex = len(p)-655
            key = p[randKeyIndex:len(p)-1]
            deckey = EnigmaMachine(key, UserKey)
            decp.append(EnigmaMachine(p[0:randKeyIndex], deckey))
    return decp


'''
salt = b'\x05;iBi\x17Q\xe0'
key_32_bytes = pbkdf2.PBKDF2("Arjun2000@!", salt).read(32)
print(ReadDecrypt(HomeDir('Data3.dat'), key_32_bytes))
'''


# searches for passwords in data3 and returns all information of required password.
def SearchFile(Str, AESkey):
    newList = []
    List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
    ind = None
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


def DelPassword(entry, AESkey):
    newListData3 = []
    Data3_List = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
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
            a = 0
            for ele in passList:
                if a == len(passList)-1:
                    passwrd += ele
                    a += 1
                else:
                    passwrd += ele + 'qwertyuiop***asdfghjklzxcvbnm'
                    a += 1
            WriteEncrypt(HomeDir('Data3.dat'), passwrd, AESkey)
    else:
        pass


def EditPassword(iniEntry, entry, AESkey):  # replaces iniEntry with entry
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
                a = 0
                for ele in passList:
                    if not a == len(passList)-1:
                        passwrd += ele + 'qwertyuiop***asdfghjklzxcvbnm'
                        a += 1
                    else:
                        passwrd += ele
                        a += 1
                WriteEncrypt(HomeDir('Data3.dat'), passwrd, AESkey)
            return False
    else:
        pass


def CheckFunction(List, LOL):
    for element in LOL:
        if List[0] == element[0]:
            return True
    return False
# print(ReadDecrypt(HomeDir('Data3.dat')))


def ShareSelected(UsernameList, CommonPassword, EntryList, AESkey):

    # Get list of all passwords from data3
    Passwords = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
    AllPasswords = []
    for i in EntryList:
        for j in Passwords:
            p = j.split("qwertyuiop***asdfghjklzxcvbnm")
            title = p[0]
            if i == title:
                AllPasswords.append(j)
    # Generate Enigma key and encrypt ALl Passwords
    Totalpassword = ''
    for password in AllPasswords:
        Enigmakey = One_Setting_Generator()
        if not AllPasswords.index(password) == len(AllPasswords) - 1:
            Totalpassword += EnigmaMachine(password, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey + '\n'
        else:
            Totalpassword += EnigmaMachine(password, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey
    # Encrypt Username list with enigma and create a string
    Totaluser = ''
    for user in UsernameList:
        Enigmakey = One_Setting_Generator()
        if UsernameList.index(user) == len(UsernameList) - 1:
            Totaluser += EnigmaMachine(user, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey
        else:
            Totaluser += EnigmaMachine(user, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey + '\n'
    Total = Totalpassword + '\n\n\n\n\n' + Totaluser

    # Generate AES key for second layer of encryption and encrypt Total
    salt = b'\x05;iBi\x17Q\xe0'
    key_AES = pbkdf2.PBKDF2(CommonPassword, salt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key_AES)
    EncryptedPasswords = aes.encrypt(Total)

    # Write Encrypted passwords in a new file
    ExportFile = open(ReminiscorFiles_Dir("Export/ShareFile.dat"), "bw")
    ExportFile.write(EncryptedPasswords)


def ShareAll(UsernameList, CommonPassword, AESkey):

    # Get list of all passwords from data3
    AllPasswords = ReadDecrypt(HomeDir('Data3.dat'), AESkey)

    # Generate Enigma key and encrypt ALl Passwords
    Totalpassword = ''
    for password in AllPasswords:
        Enigmakey = One_Setting_Generator()
        if not AllPasswords.index(password) == len(AllPasswords) - 1:
            Totalpassword += EnigmaMachine(password, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey + '\n'
        else:
            Totalpassword += EnigmaMachine(password, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey

    # Encrypt Username list with enigma and create a string
    Totaluser = ''
    for user in UsernameList:
        Enigmakey = One_Setting_Generator()
        if UsernameList.index(user) == len(UsernameList) - 1:
            Totaluser += EnigmaMachine(user, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey
        else:
            Totaluser += EnigmaMachine(user, Enigmakey) + \
                'mnbvcxzlkjhgfdsapoiuytrewq' + Enigmakey + '\n'
    Total = Totalpassword + '\n\n\n\n\n' + Totaluser

    # Generate AES key for second layer of encryption and encrypt Total
    salt = b'\x05;iBi\x17Q\xe0'
    key_AES = pbkdf2.PBKDF2(CommonPassword, salt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key_AES)
    EncryptedPasswords = aes.encrypt(Total)

    # Write Encrypted passwords in a new file
    ExportFile = open(ReminiscorFiles_Dir("Export/ShareFile.dat"), "bw")
    ExportFile.write(EncryptedPasswords)


'''UsernameList = ['Arjun', 'Manu', 'Manvendra']
CommonPassword = "Manvendra2002"
salt = b'\x05;iBi\x17Q\xe0'
AESkey = pbkdf2.PBKDF2("manvendra2", salt).read(32)
aes = pyaes.AESModeOfOperationCTR(AESkey)
ShareAll(UsernameList, CommonPassword, AESkey)'''


def GetAllPasswordTitles(AESkey):

    Data3datalist = ReadDecrypt(HomeDir('Data3.dat'), AESkey)
    Titles = []
    for Enigmapasswords in Data3datalist:
        List = Enigmapasswords.split('qwertyuiop***asdfghjklzxcvbnm')
        title = List[0]
        Titles.append(title)
    return Titles


def Import(CommonPassword, Username, AESkey):

    # Read from share file and AES decrypt
    sharedfile = open(ReminiscorFiles_Dir('Import/ShareFile.dat'), 'br')
    EncryptedSharedData = sharedfile.read()
    salt = b'\x05;iBi\x17Q\xe0'
    key_AES = pbkdf2.PBKDF2(CommonPassword, salt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key_AES)
    SharedDataBytes = aes.decrypt(EncryptedSharedData)
    SharedData = str(SharedDataBytes, 'utf-8')

    # Seperate passwords and usernames
    SharedDataList = SharedData.split('\n\n\n\n\n')
    TotalPassword = SharedDataList[0]
    Totaluser = SharedDataList[1]

    # Create enigma encrypted password list and user list
    PasswordList = TotalPassword.split('\n')
    UserList = Totaluser.split('\n')
    # Enigma decrypt all usernames
    DecryptedUsers = []
    for enigmauser in UserList:
        encrypteduserlist = enigmauser.split('mnbvcxzlkjhgfdsapoiuytrewq')
        encrypteduser = encrypteduserlist[0]
        key = encrypteduserlist[1]
        user = EnigmaMachine(encrypteduser, key)
        DecryptedUsers.append(user)

    # Check if current user is in list
    if Username in DecryptedUsers:

        # Enigma decypt passwordList
        DecryptedPasswords = []
        for enigmapassword in PasswordList:
            encryptedpasswordlist = enigmapassword.split(
                'mnbvcxzlkjhgfdsapoiuytrewq')
            encryptedpassword = encryptedpasswordlist[0]
            key = encryptedpasswordlist[1]
            password = EnigmaMachine(encryptedpassword, key)
            DecryptedPasswords.append(password)

        # Split all passwords into its components and extract the titles
        Listoftitles = []
        for password in DecryptedPasswords:
            listofthings = password.split('qwertyuiop***asdfghjklzxcvbnm')
            title = listofthings[0]
            Listoftitles.append(title)
        # Get password titles from data3
        Titles = GetAllPasswordTitles(AESkey)

        # Write all passords in Data3
        for password in DecryptedPasswords:
            if not Listoftitles[DecryptedPasswords.index(password)] in Titles:
                WriteEncrypt(HomeDir('Data3.dat'), password, AESkey)
        return True
    else:
        return False


'''
CommonPassword = "manvendra2002"
salt = b'\x05;iBi\x17Q\xe0'
AESkey = pbkdf2.PBKDF2("manvendra2", salt).read(32)
aes = pyaes.AESModeOfOperationCTR(AESkey)
print(Import(CommonPassword,'manvendra', AESkey))
'''


def Backup_Data():
    data1 = open(HomeDir("Data1.dat"), 'br')
    data1_content = data1.read()
    data1.close()
    data2 = open(HomeDir("Data2.dat"), 'br')
    data2_content = data2.read()
    data2.close()
    data3 = open(HomeDir("Data3.dat"), 'br')
    data3_content = data3.read()
    data3.close()
    dir = homedir = os.path.expanduser('~')+'/Reminiscor Files/Backup/'
    file1 = open(dir+"Data1_backup.dat", 'bw')
    file2 = open(dir+"Data2_backup.dat", 'bw')
    file3 = open(dir+"Data3_backup.dat", 'bw')
    file1.write(data1_content)
    file2.write(data2_content)
    file3.write(data3_content)
    file1.close()
    file2.close()
    file3.close()


def ImportBackup():
    dir = homedir = os.path.expanduser('~')+'/Reminiscor Files/Backup/'
    file1 = open(dir+"Data1_backup.dat", 'br')
    file2 = open(dir+"Data2_backup.dat", 'br')
    file3 = open(dir+"Data3_backup.dat", 'br')
    data1_content = file1.read()
    data2_content = file2.read()
    data3_content = file3.read()
    file1.close()
    file2.close()
    file3.close()
    data1 = open(HomeDir("Data1.dat"), "bw")
    data2 = open(HomeDir("Data2.dat"), "bw")
    data3 = open(HomeDir("Data3.dat"), "bw")
    data1.write(data1_content)
    data2.write(data2_content)
    data3.write(data3_content)
    data1.close()
    data2.close()
    data3.close()

