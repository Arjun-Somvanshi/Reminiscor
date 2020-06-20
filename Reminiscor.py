
from kivy.config import Config
Config.set('kivy','window_icon','UI/winicon.png')
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
from kivy.properties import ObjectProperty,BooleanProperty,NumericProperty
from kivy.uix.popup import Popup
from PassGen import *
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from LoginScreenResponse import *
from SignUpResponse import *
from Password_Read_Write import *
from EnigmaModule import *
from FileHandling import *
import os
import pyperclip
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
#----------------------------------------------------------------------LOGIN WINDOW------------------------------------------------------------------------------------------------------
class LoginWindow(Screen):
	username=ObjectProperty()
	p=ObjectProperty()
	errortext=ObjectProperty()
	user_check=ObjectProperty()
	def on_enter(self):
		Clock.schedule_once(self.welcome_screen)
	def welcome_screen(self,*_):
		if not CheckUser():
			design=Welcome()
			welcome_pop=Popup(title='',content=design,size_hint=(None,None),size=(400,500),separator_height=0,background='UI/Welcome.png')
			welcome_pop.open()
			design.ids.close.bind(on_release=welcome_pop.dismiss)
			welcome_pop.bind(on_dismiss=self.signup_pop)
	def welcome_screen1(self,*_):
		design=Welcome()
		welcome_pop=Popup(title='',content=design,size_hint=(None,None),size=(400,500),separator_height=0,background='UI/Welcome.png')
		welcome_pop.open()
		design.ids.close.bind(on_release=welcome_pop.dismiss)
	def close(self):
		self.win.dismiss()
	def user_error_popup(self):
		design=UserError()
		UserExists=Popup(title='User Error Encountered!',title_align='center',content=design,size_hint=(None,None),size=(400,200),separator_color=[0,171/255,174/255,1],background='UI/popup400x200.png',auto_dismiss=False)
		UserExists.open()
		design.ids.close.bind(on_release=UserExists.dismiss)
	def signup_pop(self,*_):
		design=SignUp_Pop()
		self.win=Popup(title='Sign-Up Screen',title_align='center',content=design,size_hint=(None,None),size=(400,450),separator_color=[0,171/255,174/255,1],background='UI/popup400x450.png')
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
				self.errortext.text='[u]Wrong credentials were entered. Try again![/u]'
				self.errortext.color=[204/255,0,0,1]
				ColorChange(self.username,True,'Invalid Field')	
				ColorChange(self.p,True,'Invalid Field')	
				return False
		else:
			self.username.text=''
			self.p.text=''
			self.signup_pop()  #redirect to signup page
			return False
	def help1(self):
		design=Help1()
		help1win=Popup(title='Help', content=design,size_hint=(None,None),size=(400,250),separator_color=[0,171/255,174/255,1],background='UI/popup400x400.png',auto_dismiss=False)
		help1win.open()
		design.ids.close.bind(on_release=help1win.dismiss)
class signup_error(FloatLayout):
	pass
class SignUp_Pop(FloatLayout):
	user=ObjectProperty()
	p1=ObjectProperty()
	p2=ObjectProperty()
	signup=ObjectProperty()
	cred_error=ObjectProperty()
	def check(self):
		if CheckMainPassword(self.user.text,self.p1.text,self.p2.text):
			parent_dir = os.path.expanduser('~') + '/AppData/Roaming'
			directory = "Reminiscor"
			os.makedirs(os.path.join(parent_dir, directory))
			File_dir = os.path.expanduser('~') + '/Desktop'
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
			error_win=Popup(title='Sign-Up Failed', content=errorpop,size_hint=(None,None),size=(400,250),separator_color=[0,171/255,174/255,1],background='UI/popup400x250.png')
			error_win.open()
			errorpop.ids.close.bind(on_release=error_win.dismiss)
			ColorChange(self.user,True,'Invalid')
			ColorChange(self.p1,True,'Invalid')
			ColorChange(self.p2,True,'Invalid')
			return False

class Help1(FloatLayout):
	pass
class Welcome(FloatLayout):
	pass
#----------------------------------------------------------------------Main WINDOW------------------------------------------------------------------------------------------------------

class MainWindow(Screen):
	passw=ObjectProperty()
	n=ObjectProperty()
	description=ObjectProperty()
	username=ObjectProperty()
	notes=ObjectProperty()
	def clear(self):
		self.ids.passwgen.text=''
		self.ids.passw.text=''
		self.ids.username.text=''
		self.ids.n.text=''
		self.ids.notes.text=''
		self.ids.description.text=''
	def sendgenpass(self):
		self.ids.passw.text=self.ids.passwgen.text
	def copytoclip(self):
		pyperclip.copy(self.ids.passwgen.text)
	def Import_Passwords(self):
		design=Login_Popup_import()
		explain=Label(markup=True,text='This is an [color=00abae]import process of passwords[/color], they will be added to your list if any.',text_size=(350,None),size_hint=(None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.95},font_size=14)
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design, size_hint=(None,None), size=(400,450),separator_color=[0,171/255,174/255,1],background='UI/popup400x450.png')
		design.ids.close.bind(on_release=win.dismiss)
		win.open()
	def Export_Passwords(self):
		design=Login_Popup_export()
		explain=Label(markup=True,text='This process will [color=00abae]decrypt and export your passwords.[/color]', text_size=(350,None),size_hint= (None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.95})
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design,size_hint=(None,None), size=(400,450),separator_color=[0,171/255,174/255,1],background='UI/popup400x450.png')
		design.ids.close.bind(on_release=win.dismiss)
		win.open()
	def p_size_popup(self):
		design=Password_Size_Popup()
		win=Popup(title='Entry Error!',content=design,size_hint=(None,None),size=(400,400),separator_color=[0,171/255,174/255,1],background='UI/popup400x400.png',auto_dismiss=False)
		win.open()
		design.ids.close.bind(on_release=win.dismiss)
	def random_password(self):
		pass_check=PassCheck(self.n)
		d_check=DescriptionCheck(self.description)
		if pass_check:
			self.p_size_popup()
			ColorChange(self.n,True,'Invalid\nSize')
		else:
			ColorChange(self.n,False,'Password\nSize')
			self.ids.passwgen.text=PasswordGen(int(self.n.text))
	def Add_New_Password(self):
		sep='qwertyuiop***asdfghjklzxcvbnm'
		if not DescriptionCheck(self.description) and len(self.passw.text)>=1:
			ColorChange(self.description,False,'Entry Title')
			ColorChange(self.n,False,'Password\nSize')
			ColorChange(self.passw,False,'Password')
			WriteEncrypt(HomeDir('Data3.txt'),self.description.text + sep + self.username.text + sep + self.passw.text + sep + self.notes.text)
			design=Password_Added()
			Added_pop=Popup(title='New Entry Added!',title_align='center',content=design,size_hint=(None,None),size=(400,200),separator_color=[0,171/255,174/255,1],background='UI/popup400x200.png')
			Added_pop.open()
			design.ids.close.bind(on_release=Added_pop.dismiss)
			self.description.text=''
			self.n.text=''
			self.passw.text=''
			self.username.text=''
			self.notes.text=''
		else:
			self.p_size_popup()
			ColorChange(self.description,True,'Invalid Add')
			ColorChange(self.passw,True,'Invalid Add')
	def refresh(self):
		ColorChange(self.description,False,'Entry Title')
		ColorChange(self.n,False,'Password\nSize')
		ColorChange(self.passw,False,'Password')
		self.manager.get_screen('PassDisp').showlist()

class Password_Added(FloatLayout):
	pass
class UserError(FloatLayout):
	pass
class Login_Popup_export(FloatLayout):
	def authenticate(self):
		if(CheckUser()):
			if(CheckCredentials(self.ids.username.text,self.ids.p.text)):
				self.ids.label.text='Export Successful!'
				self.ids.label.color=[0,171/255,174/255,1]
				Export()
			else:
				self.ids.label.text='Authentication Failed!'
				self.ids.label.color=[204/255,0,0,1]

class Login_Popup_import(FloatLayout):
	def authenticate(self):
		if(CheckUser()):
			if(CheckCredentials(self.ids.username.text,self.ids.p.text)):
				a=Import()
				if a==True:
					self.ids.label.text='Import Successful!'
					self.ids.label.color=[0,171/255,174/255,1]
					self.ids.label.color=[1,1,1,1]
				else:
					self.ids.label.text='Import File is not present or empty.'
					self.ids.label.pos_hint={'center_x':0.6,'center_y':0.72}
					self.ids.label.color=[204/255,0,0,1]
			else:
				self.ids.label.text='Authentication Failed!'
				self.ids.label.pos_hint={'center_x':0.75,'center_y':0.72}
				self.ids.label.color=[204/255,0,0,1]

class Password_Size_Popup(FloatLayout):
	pass

#----------------------------------------------------------------------Password WINDOW------------------------------------------------------------------------------------------------------

class Password_Screen(Screen):
	passn=None		
	def Import_Passwords(self):
		design=Login_Popup_import()
		explain=Label(markup=True,text='This is an [color=00abae]import process of passwords[/color], they will be added to your list if any.',text_size=(350,None),size_hint=(None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.95},font_size=14)
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design, size_hint=(None,None), size=(400,450),separator_color=[0,171/255,174/255,1],background='UI/popup400x450.png')
		design.ids.close.bind(on_release=win.dismiss)
		win.open()
	def Export_Passwords(self):
		design=Login_Popup_export()
		explain=Label(markup=True,text='This process will [color=00abae]decrypt and export your passwords.[/color]', text_size=(350,None),size_hint= (None, .1),width=400,pos_hint= {'center_x': 0.5, 'top': 0.95})
		design.add_widget(explain)
		win=Popup(title='Authentication Prompt',content=design,size_hint=(None,None), size=(400,450),separator_color=[0,171/255,174/255,1],background='UI/popup400x450.png')
		design.ids.close.bind(on_release=win.dismiss)
		win.open()
	def __init__(self, **kwargs):
		super(Password_Screen,self).__init__(**kwargs)
		self.mainlayout=BoxLayout(orientation='horizontal',spacing=10)
		layout0=FloatLayout()
		self.searchbar=TextInput(multiline=False,hint_text='Search for a Password', size_hint=(None,None),size =(200,40),pos_hint={'x':0,'top':1},halign='center',
			                     foreground_color=(0.7,0.7,0.7,1),color=(0.7,0.7,0.7),cursor_color=(0,171/255,174/255,1),background_color=(45/255,45/255,45/255,1))
		searchbtn=Button(size_hint=(None,None),size =(40,40),pos_hint={'x':0.51,'top':1},halign='center',on_release=self.searchresult)
		Backbtn=Button(text='Go Back', size_hint=(None,None),size=(150,96), pos_hint={'x':0,'y':0},on_release=self.screenswitch)
		searchbtn.background_normal='UI/Search.png'
		searchbtn.background_down='UI/SearchOnDown.png'
		Backbtn.background_normal='UI/Main Window Button.png'
		Backbtn.background_down='UI/Main Window Button Ondown.png'
		#self.searchbar.keyboard_on_key_up(Window,13)
		layout0.add_widget(searchbtn)
		layout0.add_widget(Backbtn)
		layout0.add_widget(self.searchbar)
		self.mainlayout.add_widget(layout0)
		self.showlist()
		self.add_widget(self.mainlayout)

	def showlist(self,*largs):
			#print('a') #to understand when show list is called 
			if len(self.mainlayout.children)>1:
				a=0
				for i in self.mainlayout.children:
					if a==0:
						self.mainlayout.remove_widget(i)
			parent=BoxLayout(orientation='vertical', spacing=10)
			layout1 = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
			layout1.bind(minimum_height=layout1.setter('height'))
			title_label=Label(text='[u][b]Entry List:[/b][/u]',markup=True, size_hint_y=None,height=60,font_size=20,color=[0,171/255,174/255,1])
			parent.add_widget(title_label)
			if os.path.isfile(HomeDir('Data3.txt')):
				password_list=ReadDecrypt(HomeDir('Data3.txt'))
				pass_len=len(password_list)
				if pass_len>0:
					for i in password_list:
						entrydata=i.split('qwertyuiop***asdfghjklzxcvbnm')
						btn = Button(text=entrydata[0],size_hint_y=None, height=60,on_release=partial(self.poppassword,entrydata))
						btn.background_normal='UI/passwordlist.png'
						btn.background_down='UI/passwordlistdown.png'
						layout1.add_widget(btn)
					root = ScrollView(size_hint=(1, 0.9), size=(Window.width, Window.height),bar_margin=2,scroll_type=['bars', 'content'],bar_width=8,bar_color=[0,171/255,174/255,1])
					root.add_widget(layout1)
					parent.add_widget(root)
					self.mainlayout.add_widget(parent)
				else:
					btn = Button(text='No passwords yet!',size_hint_y=None, height=60,color=[204/255,0,0,1])
					btn.background_normal='UI/Main Window Button.png'
					btn.background_down='UI/Main Window Button.png'
					root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
					layout1.add_widget(btn)
					root.add_widget(layout1)
					parent.add_widget(root)
					self.mainlayout.add_widget(parent)
			else:
				btn = Button(text='No passwords yet!',size_hint_y=None, height=60)
				btn.background_normal='UI/Main Window Button.png'
				btn.background_down='UI/Main Window Button.png'
				root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
				layout1.add_widget(btn)
				root.add_widget(layout1)
				parent.add_widget(root)
				self.mainlayout.add_widget(parent)

	def searchresult(self,instance):
		result=SearchFile(self.searchbar.text)
		if result==[]:
			design=search_popup()
			design.ids.title.text='No such entry exists'
			design.ids.username.text='No such entry exists'
			design.ids.password.text='No such entry exists'
			design.ids.notes.text='No such entry exists'
			search=Popup(title='Search result',title_align='center',content=design,size_hint=(None,None),size=(400,400),separator_color=[0,171/255,174/255,1],background='UI/popup400x400.png',auto_dismiss=False)
			search.open()
			design.ids.close.bind(on_release=partial(self.DismissAndTriggerCancel,design,search))
		else:
			design=search_popup()
			design.ids.title.text=result[0]
			design.ids.username.text=result[1]
			design.ids.password.text='Password: '
			design.ids.password.text=result[2]
			design.ids.notes.text=result[3]
			search=Popup(title='Search result',title_align='center',content=design,size_hint=(None,None),size=(400,400),separator_color=[0,171/255,174/255,1],background='UI/popup400x400.png')
			search.open()
			design.ids.close.bind(on_release=partial(self.DismissAndTriggerCancel,design,search))
			design.ids.delete.bind(on_release=partial(self.DeleteAndRefresh,design,search))
			design.ids.edit.bind(on_release=partial(self.editflow,design,result))
		self.searchbar.text=''
	def screenswitch(self,instance):
		self.manager.transition=SlideTransition()
		self.manager.current = 'Main'
		self.manager.transition.direction='right'
	def poppassword(self,entrydata,*args):
		design=passwordpopup()
		design.ids.title.text+=entrydata[0]
		design.ids.username.text+=entrydata[1]
		design.ids.password.text+=entrydata[2]
		design.ids.notes.text+=entrydata[3]
		entry=Popup(title='Entry Information',title_align='center',content=design,size_hint=(None,None),size=(400,400),separator_color=[0,171/255,174/255,1],background='UI/popup400x400.png',auto_dismiss=False)
		entry.open()
		design.ids.close.bind(on_release=partial(self.DismissAndTriggerCancel,design,entry))
		design.ids.delete.bind(on_release=partial(self.DeleteAndRefresh,design,entry))
		design.ids.edit.bind(on_release=partial(self.editflow,design,entrydata))
	def editflow(self,design,entrydata,instance):
		editconfirm=Edit_Confirmation()
		editwin=Popup(title='Edit Confirmation', content=editconfirm,size_hint=(None,None),size=(400,200),separator_color=[0,171/255,174/255,1],background='UI/popup400x200.png',auto_dismiss=False)		
		editwin.open()
		editconfirm.ids.close.bind(on_release=editwin.dismiss)
		editconfirm.ids.yes.bind(on_release=partial(self.confirm2,design,entrydata,editwin))
	def confirm2(self,design,entrydata,editwin,*_):
		check=design.edit(entrydata)
		if check:
			design.ids.title.text=entrydata[0]
		editwin.dismiss()
		self.showlist()
	def DismissAndTriggerCancel(self,design,entry,instance):
		entry.dismiss()
	def DeleteAndRefresh(self,design,entry,instance):
		self.check=False
		deletepop=Delete_Confirmation()
		deletewin=Popup(title='Delete Confirmation', content=deletepop,size_hint=(None,None),size=(400,200),separator_color=[0,171/255,174/255,1],background='UI/popup400x200.png',auto_dismiss=False)
		deletewin.open()
		deletepop.ids.close.bind(on_release=deletewin.dismiss)
		deletepop.ids.yes.bind(on_release=partial(self.confirm1,design,entry,deletewin))
	def confirm1(self,design,entry,deletewin,*args):
		design.delete()
		deletewin.dismiss()
		entry.dismiss()
		self.showlist()
class passwordpopup(FloatLayout):
	viewing = BooleanProperty(True)
	def delete(self, *args):
		entry=[]
		entry.append(self.ids.title.text)
		entry.append(self.ids.username.text)
		entry.append(self.ids.password.text)
		entry.append(self.ids.notes.text)
		DelPassword(entry)
	def copytoclip1(self):
		pyperclip.copy(self.ids.username.text)
	def copytoclip2(self):
		pyperclip.copy(self.ids.password.text)
	def edit(self,entrydata):
		self.ids.edittoggle.state='normal'
		editedentry=[]
		editedentry.append(self.ids.title.text)
		editedentry.append(self.ids.username.text)
		editedentry.append(self.ids.password.text)
		editedentry.append(self.ids.notes.text)
		check=EditPassword(entrydata,editedentry)
		return check

class search_popup(FloatLayout):
	viewing = BooleanProperty(True)
	def delete(self, *args):
		print('deleted')
		entry=[]
		entry.append(self.ids.title.text)
		entry.append(self.ids.username.text)
		entry.append(self.ids.password.text)
		entry.append(self.ids.notes.text)
		DelPassword(entry)
	def copytoclip1(self):
		pyperclip.copy(self.ids.username.text)
	def copytoclip2(self):
		pyperclip.copy(self.ids.password.text)
	def edit(self,entrydata):
		print('flow')
		self.ids.edittoggle.state='normal'
		editedentry=[]
		editedentry.append(self.ids.title.text)
		editedentry.append(self.ids.username.text)
		editedentry.append(self.ids.password.text)
		editedentry.append(self.ids.notes.text)
		check=EditPassword(entrydata,editedentry)
		return check
class Delete_Confirmation(FloatLayout):
	pass
class Edit_Confirmation(FloatLayout):
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