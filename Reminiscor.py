
from kivy.config import Config
Config.set('kivy','window_icon','UI\\winicon.png')
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'default_font', '["Montserrat", "Fonts/Montserrat-Regular.ttf", "Fonts/Montserrat-Regular.ttf", "Fonts/Montserrat-Bold.ttf", "Fonts/Montserrat-Bold.ttf"]')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
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
Window.clearcolor = (30/255, 30/255, 30/255, 1)
from functools import partial

MonitorData2=None
if os.path.isfile(HomeDir('Data2.txt')):
	MonitorData2=ModifiedFileTime(HomeDir('Data2.txt'))
else:
	MonitorData2=None
class search_popup(FloatLayout):
	pass
class signup_error(FloatLayout):
	pass
class Password_Added(FloatLayout):
	pass
class UserError(FloatLayout):
	pass
class Password_Size_Popup(FloatLayout):
	pass
class Login_Popup_export(FloatLayout):
	def authenticate(self):
		if(CheckUser()):
			if(CheckCredentials(self.ids.username.text,self.ids.p.text)):
				self.ids.label.text='Export Successful.'
				self.ids.label.color=[1,1,1,1]
				Export()
			else:
				self.ids.label.text='Authentication Failed.'
				self.ids.label.color=[1,0,0,1]
class Login_Popup_import(FloatLayout):
	def authenticate(self):
		if(CheckUser()):
			if(CheckCredentials(self.ids.username.text,self.ids.p.text)):
				a=Import()
				if a==True:
					self.ids.label.text='Import Successful.'
					self.ids.label.color=[1,1,1,1]
				else:
					self.ids.label.text='Import File is not present.'
					self.ids.label.color=[1,0,0,1]
			else:
				self.ids.label.text='Authentication Failed'
				self.ids.label.color=[1,0,0,1]
				self.add_widget(label)
				
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
			File_dir = os.path.expanduser('~') + '\\Desktop'
			direc = "Reminiscor Export_Import"
			os.makedirs(os.path.join(File_dir, direc))
			Default_Unique_User_EnigmaSettings()
			global MonitorData2 
			MonitorData2=ModifiedFileTime(HomeDir('Data2.txt'))
			sep='qwertyuiop***asdfghjklzxcvbnm'
			file=open(HomeDir('Data1.txt'),'w')
			file.close()
			#HideFile(HomeDir('Data1.txt'))
			file=open(HomeDir('Data3.txt'),'w')
			file.close()
			#`HideFile(HomeDir('Data3.txt'))
			WriteEncrypt(HomeDir('Data1.txt'),self.user.text+sep+self.p1.text)
			label=Label(text='You\'ve successfully signed up!', size_hint=(0.1,0.1), pos_hint={'center_x':0.5,'center_y':0.225})
			self.add_widget(label)
			ColorChange(self.user,False,'Username')
			ColorChange(self.p1,False,'Master Password')
			ColorChange(self.p2,False,'Confirm Master Passwords')
			return True
		else:
			errorpop=signup_error()
			error_win=Popup(title='Sign-Up Failed', content=errorpop,size_hint=(None,None),size=(400,250))
			error_win.open()
			errorpop.ids.close.bind(on_release=error_win.dismiss)
			ColorChange(self.user,True,'Invalid')
			ColorChange(self.p1,True,'Invalid')
			ColorChange(self.p2,True,'Invalid')
			return False

class LoginWindow(Screen):
	username=ObjectProperty()
	p=ObjectProperty()
	errortext=ObjectProperty()
	user_check=ObjectProperty()
	def close(self):
		self.win.dismiss()
	def user_error_popup(self):
		design=UserError()
		UserExists=Popup(title='User Error Encountered!',title_align='center',content=design,size_hint=(None,None),size=(400,200))
		UserExists.open()
	def signup_pop(self):
		design=SignUp_Pop()
		self.win=Popup(title='Sign-Up Screen',title_align='center',content=design,size_hint=(None,None),size=(400,450))
		self.win.open()
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
	def Import_Passwords(self):
		design=Login_Popup_import()
		explain=Label(text='This is an import process of passwords, they will be added to your list if any.', text_size=(350,None),size_hint=(None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.95})
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design, size_hint=(None,None), size=(400,450))
		win.open()
	def Export_Passwords(self):
		design=Login_Popup_export()
		explain=Label(text='This process will decrypt and export your passwords.', text_size=(350,None),size_hint= (None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.9})
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design,size_hint=(None,None), size=(400,450))
		win.open()
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
			ColorChange(self.description,True,'Invalid Size/Title')
		else:
			ColorChange(self.n,False,'Password\nSize')
			ColorChange(self.description,False,'Entry Title')
			self.passw.text=PasswordGen(int(self.n.text))
	def Add_New_Password(self):
		sep='qwertyuiop***asdfghjklzxcvbnm'
		if not DescriptionCheck(self.description) and len(self.passw.text)>=1:
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
	def refresh(self):
		self.manager.get_screen('PassDisp').showlist()
		pass
class Password_Screen(Screen):
	passn=None		

	def __init__(self, **kwargs):
		super(Password_Screen,self).__init__(**kwargs)
		self.refreshing=False
		self.mainlayout=BoxLayout(orientation='horizontal',spacing=10)
		layout0=FloatLayout()
		self.searchbar=TextInput(multiline=False,hint_text='Search for a Password', size_hint=(None,None),size =(200,40),pos_hint={'x':0,'top':1},halign='center',
			                     foreground_color=(0.7,0.7,0.7,1),color=(0.7,0.7,0.7),cursor_color=(0,171/255,174/255,1),background_color=(45/255,45/255,45/255,1))
		searchbtn=Button(size_hint=(None,None),size =(40,40),pos_hint={'x':0.51,'top':1},halign='center',on_release=self.searchresult)
		Backbtn=Button(text='Go Back', size_hint=(.3,.08), pos_hint={'x':0,'y':0},on_release=self.screenswitch)
		searchbtn.background_normal='UI/Search.png'
		searchbtn.background_down='UI/SearchOnDown.png'
		Backbtn.background_normal='UI/button for login.png'
		Backbtn.background_down='UI/on down login.png'
		layout0.add_widget(searchbtn)
		layout0.add_widget(Backbtn)
		layout0.add_widget(self.searchbar)
		self.mainlayout.add_widget(layout0)
		self.showlist()
		#Clock.schedule_interval(partial(self.showlist ),0.5)
		self.add_widget(self.mainlayout)
	def showlist(self,*largs):
			print('a')
			if len(self.mainlayout.children)>1:
				a=0
				for i in self.mainlayout.children:
					if a==0:
						self.mainlayout.remove_widget(i)
			layout1 = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
			layout1.bind(minimum_height=layout1.setter('height'))
			if os.path.isfile(HomeDir('Data3.txt')):
				password_list=ReadDecrypt(HomeDir('Data3.txt'))
				pass_len=len(password_list)
				if pass_len>0:
					for i in password_list:
						entrydata=i.split('qwertyuiop***asdfghjklzxcvbnm')
						btn = Button(text=entrydata[0],size_hint_y=None, height=60,on_release=partial(self.poppassword,entrydata))
						btn.background_normal='UI/Main Window Button.png'
						btn.background_down='UI/Main Window Button Ondown.png'
						layout1.add_widget(btn)
					root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
					root.add_widget(layout1)
					self.mainlayout.add_widget(root)
				else:
					btn = Button(text='No passwords yet!',size_hint_y=None, height=60,color=[1,0,0,1])
					btn.background_normal='UI/Main Window Button.png'
					btn.background_down='UI/Main Window Button.png'
					root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
					layout1.add_widget(btn)
					root.add_widget(layout1)
					self.mainlayout.add_widget(root)

			else:
				btn = Button(text='No passwords yet!',size_hint_y=None, height=60)
				btn.background_normal='UI/Main Window Button.png'
				btn.background_down='UI/Main Window Button.png'
				root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
				layout1.add_widget(btn)
				root.add_widget(layout1)
				mainlayout.add_widget(root)
	def searchresult(self,instance):
		result=SearchFile(self.searchbar.text)
		if result==[]:
			design=search_popup()
			design.ids.title.text='No such entry exists'
			search=Popup(title='Search result',title_align='center',content=design,size_hint=(None,None),size=(400,400))
			search.open()
		else:
			design=search_popup()
			design.ids.title.text='Title: '+result[0]
			design.ids.username.text='Title: '+result[1]
			design.ids.passtext.text='Password: '
			design.ids.password.text=result[2]
			design.ids.notes.text='Notes: '+result[3]
			search=Popup(title='Search result',title_align='center',content=design,size_hint=(None,None),size=(400,400))
			search.open()
	def screenswitch(self,instance):
		if self.refreshing:
			self.refresh_event.cancel()
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
		design.ids.delete.bind(on_release=entry.dismiss)
		self.refresh_event = Clock.schedule_interval(self.showlist, 0.5)
		self.refreshing=True
class editpopup(FloatLayout):
	def pre_edit(self):
		self.entrydata=[]
		self.entrydata.append(self.ids.title_input.text)
		self.entrydata.append(self.ids.username_input.text)
		self.entrydata.append(self.ids.password.text)
		self.entrydata.append(self.ids.notes_input.text)
	def edit(self):
		entry=[]
		entry.append(self.ids.title_input.text)
		entry.append(self.ids.username_input.text)
		entry.append(self.ids.password.text)
		entry.append(self.ids.notes_input.text)
		EditPassword(self.entrydata,entry)
class passwordpopup(FloatLayout):
	def edit_popup(self):
		design=editpopup()
		design.ids.title_input.text+=self.ids.title.text
		design.ids.username_input.text+=self.ids.username.text
		design.ids.password.text+=self.ids.password.text
		design.ids.notes_input.text+=self.ids.notes.text
		design.pre_edit()
		entry=Popup(title='Entry Information',title_align='center',content=design,size_hint=(None,None),size=(400,400))
		entry.open()
	def delete(self):
		entry=[]
		entry.append(self.ids.title.text)
		entry.append(self.ids.username.text)
		entry.append(self.ids.password.text)
		entry.append(self.ids.notes.text)
		DelPassword(entry)
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