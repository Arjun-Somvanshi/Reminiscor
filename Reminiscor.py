
from kivy.config import Config
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from PassGen import *
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.lang import Builder
from LoginScreenResponse import *
from SignUpResponse import *
from Password_Read_Write import *
from EnigmaModule import *
from FileHandling import *
import os
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from functools import partial

MonitorData2=None
if os.path.isfile(HomeDir('Data2.txt')):
	MonitorData2=ModifiedFileTime(HomeDir('Data2.txt'))
else:
	MonitorData2=None
class Password_Added(FloatLayout):
	pass
class UserError(FloatLayout):
	pass
class Password_Size_Popup(FloatLayout):
	pass
class SignUp_Pop(FloatLayout):
	user=ObjectProperty()
	p1=ObjectProperty()
	p2=ObjectProperty()
	signup=ObjectProperty()
	cred_error=ObjectProperty()
	def check(self):
		if CheckMainPassword(self.user.text,self.p1.text,self.p2.text):
			parent_dir = os.path.expanduser('~') + '\\AppData\\Roaming'
			directory = "Reminiscor"
			os.mkdir(os.path.join(parent_dir, directory))
			Default_Unique_User_EnigmaSettings()
			global MonitorData2 
			MonitorData2=ModifiedFileTime(HomeDir('Data2.txt'))
			sep='qwertyuiop***asdfghjklzxcvbnm'
			file=open(HomeDir('Data1.txt'),'w')
			file.close()
			HideFile(HomeDir('Data1.txt'))
			file=open(HomeDir('Data3.txt'),'w')
			file.close()
			HideFile(HomeDir('Data3.txt'))
			WriteEncrypt(HomeDir('Data1.txt'),self.user.text+sep+self.p1.text)
			self.cred_error.text='You\'ve successfully signed up!'
			self.cred_error.color=[1,1,1,1]
			ColorChange(self.user,False,'Username')
			ColorChange(self.p1,False,'Master Password')
			ColorChange(self.p2,False,'Confirm Master Passwords')
			return True
		else:
			self.cred_error.color=[1,0,0,1]
			self.cred_error.text='A Username should contain 8 characters.\nPasswords should match and contain atleast 10 characters.'
			ColorChange(self.user,True,'Invalid')
			ColorChange(self.p1,True,'Invalid')
			ColorChange(self.p2,True,'Invalid')
			return False

class LoginWindow(Screen):
	username=ObjectProperty()
	p=ObjectProperty()
	errortext=ObjectProperty()
	user_check=ObjectProperty()
	def user_error_popup(self):
		design=UserError()
		UserExists=Popup(title='User Error Encountered!',title_align='center',content=design,size_hint=(None,None),size=(400,200))
		UserExists.open()
	def signup_pop(self):
		design=SignUp_Pop()
		win=Popup(title='Sign-Up Screen',title_align='center',content=design,size_hint=(None,None),size=(400,450))
		win.open()
	def signup_check(self):
		if not CheckUser():
			self.signup_pop()
		else:
			self.user_error_popup()
	def Login_Authenticate(self):
		if CheckUser():
			if CheckCredentials(self.username.text,self.p.text):    #To check if main credential file exists
				self.user_check.text=''
				self.errortext.text=''
				self.errortext.color=[1,1,1,1]
				self.username.text=''
				self.p.text=''
				ColorChange(self.username,False,'Username')	
				ColorChange(self.p,False,'Master Password')
				return True 
			else:
				self.errortext.text='Wrong credentials were entered. Try again.'
				self.errortext.color=[1,0,0,1]
				ColorChange(self.username,True,'Invalid Field')	
				ColorChange(self.p,True,'Invalid Field')	
				return False
		else:
			self.username.text=''
			self.p.text=''
			self.signup_pop()  #redirect to signup page
			return False

class MainWindow(Screen):
	passw=ObjectProperty()
	n=ObjectProperty()
	description=ObjectProperty()
	username=ObjectProperty()
	notes=ObjectProperty()
	def p_size_popup(self):
		design=Password_Size_Popup()
		win=Popup(title='Error',content=design,size_hint=(None,None),size=(400,400))
		win.open()
	def random_password(self):
		pass_check=PassCheck(self.n)
		d_check=DescriptionCheck(self.description)
		if pass_check and d_check:
			self.p_size_popup()
			ColorChange(self.n,True,'Invalid\nSize')
			ColorChange(self.description,True,'Invalid Size')
		elif pass_check is True and d_check is False:
			self.p_size_popup()
			ColorChange(self.description,False)
			ColorChange(self.n,True,'Invalid\nSize')
		elif d_check is True and pass_check is False:
			self.p_size_popup()
			ColorChange(self.n,False)
			ColorChange(self.description,True,'Invalid Size')
		else:
			ColorChange(self.n,False,'Password\nSize')
			ColorChange(self.description,False,'Entry Title')
			self.passw.text=PasswordGen(int(self.n.text))
	def Add_New_Password(self):
		sep='qwertyuiop***asdfghjklzxcvbnm'
		if not DescriptionCheck(self.description) and len(self.passw.text)>=8:
			ColorChange(self.description,False,'Entry Title')
			ColorChange(self.n,False,'Password\nSize')
			ColorChange(self.passw,False,'Password')
			if self.username.text=='':
				self.username.text='     '
			if self.notes.text=='':
				self.notes.text='     '
			WriteEncrypt(HomeDir('Data3.txt'),self.description.text + sep + self.username.text + sep + self.passw.text + sep + self.notes.text)
			design=Password_Added()
			Added_pop=Popup(title='Password Added!',title_align='center',content=design,size_hint=(None,None),size=(400,200))
			Added_pop.open()
			self.description.text=''
			self.n.text=''
			self.passw.text=''
			self.username.text=''
			self.notes.text=''
		else:
			ColorChange(self.description,True,'Invalid Add')
			ColorChange(self.n,True,'Invalid\nAdd')
			ColorChange(self.passw,True,'Invalid Add')
	def screen3(self):
		x=Password_Screen()
class Password_Screen(Screen):
	passn=None
	def __init__(self, **kwargs):
		super(Password_Screen,self).__init__(**kwargs)
		def showlist(*args):
			if len(mainlayout.children)>1:
				a=0
				for i in mainlayout.children:
					if a==0:
						mainlayout.remove_widget(i)
			password_list=ReadDecrypt(HomeDir('Data3.txt'))
			pass_len=len(password_list)
			layout1 = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
			layout1.bind(minimum_height=layout1.setter('height'))
			if pass_len>0:
				for i in password_list:
					entrydata=i.split('qwertyuiop***asdfghjklzxcvbnm')
					btn = Button(text=entrydata[0],size_hint_y=None, height=60,on_release=partial(self.poppassword,entrydata))
					layout1.add_widget(btn)
				root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
				root.add_widget(layout1)
				mainlayout.add_widget(root)
			else:
				btn = Button(text='No passwords yet!',size_hint_y=None, height=60)
				root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
				layout1.add_widget(btn)
				root.add_widget(layout1)
				mainlayout.add_widget(root)
		
		mainlayout=BoxLayout(orientation='horizontal',spacing=10)
		layout0=FloatLayout()
		searchbar=TextInput(multiline=False,hint_text='Search for a Password', size_hint=(None,None),size =(250,40),pos_hint={'center_x':0.5,'top':1},halign='center')
		Backbtn=Button(text='Go Back', size_hint=(.3,.08), pos_hint={'x':0,'y':0},on_release=self.screenswitch)
		Refreshbtn=Button(text='Refresh List', size_hint=(.3,.08), pos_hint={'x':0.5,'y':0},on_release=showlist)
		layout0.add_widget(Refreshbtn)
		layout0.add_widget(Backbtn)
		layout0.add_widget(searchbar)
		mainlayout.add_widget(layout0)
		if os.path.isfile(HomeDir('Data3.txt')):
			showlist()
		self.add_widget(mainlayout)
		
	def screenswitch(self,instance):
		self.manager.current = 'Main'
		self.manager.transition.direction='right'
	def poppassword(self,entrydata,*args):
		design=passwordpopup()
		design.ids.title.text+=entrydata[0]
		design.ids.username.text+=entrydata[1]
		design.ids.password.text+=entrydata[2]
		design.ids.notes.text+=entrydata[3]
		entry=Popup(title='Entry Information',title_align='center',content=design,size_hint=(None,None),size=(400,400))
		entry.open()
class passwordpopup(FloatLayout):
	pass
class Screen_Manager(ScreenManager):
	pass
kv=Builder.load_file("reminiscorGUI.kv")
class ReminiscorApp(App):
	def destruct(self, dt):
		global MonitorData2
		if os.path.isfile(HomeDir('Data2.txt')):
			if CheckModified(MonitorData2,ModifiedFileTime(HomeDir('Data2.txt'))) and not MonitorData2==None:
				self.get_running_app().stop()
	def build(self):
		Clock.schedule_interval(self.destruct, 1.0/60.0)
		return kv
if __name__ == '__main__':
	ReminiscorApp().run()