from FileHandling import *
#This compares password and confirm password 
def CheckMainPassword(usrName, paswrd, repaswrd):

    if paswrd == repaswrd and len(usrName) >= 8 and len(usrName) <= 50 and len(paswrd)>=8 and paswrd!=usrName:
    	for i in usrName:
    		if i ==',':
    			return False
    		else:
        		return True
    else:
        return False





