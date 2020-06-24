#Module which generates password
import string
from random import randint
from Password_Read_Write import *
from FileHandling import *
def ColorChange(n,error,error_text='',color=(45/255,45/255,45/255,1)):
	if error:
		n.background_color=(204/255, 0, 0,1)				
		n.hint_text_color=(0.2,0.2,0.2,1)
		n.cursor_color=(0,0,0,1)
		n.hint_text=error_text 
	else:
		n.background_color=color
		n.hint_text_color=(0.5, 0.5, 0.5, 1.0)
		n.cursor_color=(0,171/255,174/255,1)
		n.hint_text=error_text


def DescriptionCheck(description,key):
	minimum_size=3
	maximum_size=30
	if os.stat(HomeDir('Data3.dat')).st_size == 0 and len(description.text)>minimum_size and len(description.text)<maximum_size:
		return False
	else:

		used=False
		entrylist=ReadDecrypt(HomeDir('Data3.dat'),key)
		for entry in entrylist:
			title=entry.split('qwertyuiop***asdfghjklzxcvbnm')
			if description.text.lower()==title[0].lower():
				used=True
				break	
		if len(description.text)<minimum_size or len(description.text)>maximum_size or used:
			return True
		else:
			return False
def PassCheck(n):
	minimum_size=8
	maximum_size=50
	if n.text.isnumeric():
		if n.text=='' or n.text.isalpha() or int(n.text)<minimum_size or int(n.text)>maximum_size:
			return True
		else:
			return False
	else:
		return True


def PasswordGen(n):
	password=''
	while True:
		a=randint(0,n-1)
		b=randint(0,n-1)
		c=randint(0,n-1)
		d=randint(0,n-1)
		if a!=b and b!=c and c!=a and d!=a and d!=b and d!=c:
			break
	for i in range(0,n):
		choice=randint(32,126)
		password+=chr(choice)
	passlist=list(password)
	passlist[a]=chr(randint(65,90))
	passlist[b]=chr(randint(48,57))
	special_char_int=list(string.punctuation+' ')
	choice=randint(0,len(special_char_int)-1)
	passlist[c]=special_char_int[choice]
	passlist[d]=chr(randint(97,122))
	password = ''.join(passlist)
	return password