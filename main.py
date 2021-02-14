from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import CardTransition, FadeTransition, FallOutTransition, NoTransition, RiseInTransition, Screen, ScreenManager, SlideTransition, SwapTransition, WipeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from functools import partial
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty, BooleanProperty
from response import *
from kivy.logger import Logger, LOG_LEVELS
Logger.setLevel(LOG_LEVELS["debug"])
#Parameters for the app
Window.clearcolor = (30/255,30/255,30/255,1)
if platform != 'android' and 1==0:
    Window.minimum_width = dp(490)
    Window.minimum_height = dp(550)

'''-------------------Global------------------------------'''
app = None
app_path = None
external_path = None
no_user = None
def quickmessage(title, message, *args):
    design = QuickMessage()
    design.ids.message.text = message
    if app._platform == 'android':
        max_size = (dp(400), dp(250))
        min_size = (dp(300), dp(250))
    else:
        max_size = (dp(400), dp(225))
        min_size = (dp(300), dp(225))
    Logger.debug('max size: %s', max_size)
    app.create_popup(max_size, min_size, True, design, title,(0.5, 0.5))
    design.ids.close.bind(on_release=app.close_popup)
'''-------------------------------------------------------'''

'''-----------------Custom Classes-----------------------'''
class CustomTextInput(TextInput):
    def on_parent(self, *_):
        self._refresh_text(self.text)

class CustomPopup(Popup):
    
    def open(self, animate = True, *largs, **kwargs):
        global app
        if animate and app.animations:
            self.disabled = True
            size_hint_y = self.size_hint_y
            max_y = self.size_hint_max_y
            self.size_hint_max_y = dp(3000)
            self.size_hint_y = 4*size_hint_y
            self.opacity = 0
            anim = Animation(size_hint_y = size_hint_y, size_hint_max_y = max_y, opacity=1, duration = 0.5)
            anim.start(self)
            anim.bind(on_complete=self.enable_popup)
        super(CustomPopup, self).open(*largs, **kwargs)
    
    def enable_popup(self, *args):
        self.disabled = False

    def dismiss(self, animate = True, *largs, **kwargs):
        self.disabled = True
        if animate and app.animations:
            anim = Animation(size_hint_y = self.size_hint_y*4,size_hint_max_y = dp(3000), opacity=0, duration = 0.5)
            anim.start(self)
            anim.bind(on_complete=self.finish_dismiss) 
        else:
            super(CustomPopup, self).dismiss()
    def finish_dismiss(self, instance, *args):
        super(CustomPopup,self).dismiss()

class CustomModalView(ModalView): # here I have made a custom modal view so that it can handle animations 
                                  # instead of typing the whole deal over and over, the open and dismiss are new                  
    def open(self, pos_hint_initial = {}, pos_hint_final = {}, 
             t = '', d1=0.7, d2=0.7, animate = True, *largs, **kwargs):
        global app
        #print(app.animations)
        if animate and app.animations: # we have to parameters to decide whether animation should occur or
        # not, incase, the user decides to not use animations on slow hardware, app.animations will be set to false, 
        # if the developer doen't wanna use the animation then he/she can set animate to false
            self.disabled = True
            self.pos_hint = pos_hint_initial
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 1, t=t, duration=d2)
            anim.start(self)
            anim.bind(on_complete=self.enable_popup)
        else: 
            self.opacity = 1
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        super(CustomModalView, self).open(*largs, **kwargs)
    
    def enable_popup(self, *args):
        self.disabled = False
    
    def dismiss(self, pos_hint_final = {}, t = '', d1=0.7, d2=0.75, animate = True, *largs, **kwargs):
        #print('dismissing')
        self.disabled = True
        if animate and app.animations:
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 0, t=t, duration = d2)
            anim.start(self)
            anim.bind(on_complete = self.finish_dismiss) # binding the on_complete callback, to finish dismiss()
        else:
            super(CustomModalView, self).dismiss()

    def finish_dismiss(self, *args):
        super(CustomModalView, self).dismiss()
'''------------------------------------------------------'''


'''--------------------Popups-----------------------------'''
class Signup(BoxLayout):
    def on_keyfile_enable(self, value, *args):
        if self.ids.enable.state == 'down':
            message = '''A KeyFile adds an extra layer of security apart from the master password. You are supposed to store this file on external hardware securely. If you lose this file your database of passwords will be [color=00abae]lost forever.[/color] If you still decide to enable this feature, you will be asked to provide a path to the keyfile after Signup, this is the path where Reminiscor will look for the file. To know more take the tutorial.'''
            global app
            design = QuickMessage()
            design.ids.message.text = message
            design.ids.close.size_hint_x = 0.5
            design.ids.close.text = 'I have read the text'
            design.ids.close.bind(on_release=app.close_popup)
            app.create_popup( (dp(400), dp(400)), (dp(400), dp(400)), True, design, 'What is a KeyFile?', (0.5,0.5))
    
    def on_confirm(self):
        self.ids.username.background_color = app.color['middle']
        self.ids.password.background_color = app.color['middle']
        self.ids.c_password.background_color = app.color['middle']
        result = signup_response(self.ids.username.text, self.ids.password.text, self.ids.c_password.text)
        if 0 in result:
            if result[0] == 0: # meaning the username is less than 3 chars
                self.ids.username.background_color = (1,1,1,1)
                self.ids.username.background_normal = 'UI/Mainbuttondown.png'
                self.ids.username.background_active = 'UI/Mainbuttondown.png'
                quickmessage('Username Error', "Your username should be atleast 3 characters long")
            elif result[1] == 0: # password less than 8
                self.ids.password.background_color = app.color['error']
                quickmessage('Master Password Error', "Your password should be atleast 8 characters long")
            elif result[2] == 0: # password do not match
                self.ids.password.background_color = app.color['error']
                self.ids.c_password.background_color = app.color['error']
                quickmessage('Password Match Error', "Your passwords do not match!")
            return False
        else:
            global no_user
            no_user = False
            return True

class Welcome(BoxLayout):
    text = StringProperty('')
    def __init__(self, **kwargs):
        super(Welcome, self).__init__(**kwargs)
        file = open('welcome.txt', 'r')
        self.text = '\n'.join(ReadFile(file))
        file.close()

class Tutorial(BoxLayout):
    text = StringProperty('')

class QuickMessage(BoxLayout):
    pass
'''-------------------------------------------------------'''
class Login(Screen):
    # This function is called when the user uses the app for the first time
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        pass
    def refactor_layout(self, signup, design):
        design.ids.keyfile.remove_widget(design.ids.enable)
    def welcome(self, *args):
        Logger.debug('Welcome was called')
        welcome_design = Welcome()
        welcome = CustomModalView(
                                size_hint = (0.7, 0.8),
                                auto_dismiss = False,
                                size_hint_max = (dp(450),dp(550)),
                                size_hint_min = (dp(325),dp(400)),
                                background = 'UI/popup400x400.png',
                                opacity = 0,
                                pos_hint = {'center_x': -2, 'center_y':0.5 }
                           )
        welcome.add_widget(welcome_design)
        self.final_dismiss_pos_hint = {'center_x': -2, 'center_y':0.5 } # this just saves space look in tutorial 
        # binding the close button with the dismiss function defined in modal view for animations
        welcome_design.ids.close.bind(on_release= partial(welcome.dismiss,self.final_dismiss_pos_hint, 'in_expo', 0.7, 0.75, True))
        if no_user:
            welcome_design.ids.close.bind(on_release=self.first_signup)# if the user uses the app for the first time, signup shows up after welcome
        # binding take the tutorial button with self.tutorial, to close the window popup
        # and then activate the tutorial
        welcome_design.ids.tutorial.bind(on_release = partial(self.tutorial_initiate, welcome))
        welcome.open(welcome.pos_hint, {'center_x': 0.5, 'center_y': 0.5}, "out_expo")

    # This is a guided tutorial for reminiscor
    def tutorial_initiate(self, welcome, instance):
        global app
        welcome.dismiss(self.final_dismiss_pos_hint, 'in_expo', 0.7, 0.75, True)
        Clock.schedule_once(self.tutorial, 0.8)
    def tutorial(self, *args):
        design = Tutorial()
        with open('tutorial.json') as f:
            design.text = ' '.join(json.load(f)['tutorials']['tutorial1']['content'])
        app.create_popup((dp(450),dp(550)), (dp(325), dp(400)), False, design, 'T U T O R I A L')
        design.ids.exit.bind(on_release = app.close_popup)
    
    def first_signup(self, *args):
        '''function to invoke signup after welcome view is dismissed, this happens only when there is no user assigned to the app'''
        Clock.schedule_once(self.call_signup, 0.75)
    # Function to invoke signup
    def call_signup(self, *args):             
        rem_exists = check_user()
        if rem_exists is not True:
            design = Signup()
            self.signup = CustomModalView(
                                size_hint = (0.5, 0.8),
                                auto_dismiss = False,
                                size_hint_max = (dp(450),dp(500)),
                                size_hint_min = (dp(325),dp(400)),
                                background = 'UI/popup400x400.png',
                                opacity = 0,
                                pos_hint = {'center_x': 0.5, 'center_y': 2}
                            )
            self.signup.add_widget(design)
            final_dismiss_welcome_pos_hint = {'center_x': 0.5, 'center_y': -2}
            design.ids.close.bind(on_release = partial(self.signup.dismiss, final_dismiss_welcome_pos_hint,
                                'in_expo', 0.7, 0.85, True))
            design.ids.enable.bind(active = design.on_keyfile_enable)
            design.ids.confirm.bind(on_release=partial(self.signup_complete, design))# had to make a separate function for confirm
            if platform =='android':
                self.refactor_layout(self.signup, design)
            Logger.debug('Signup was called here')
            self.signup.open(self.signup.pos_hint, {'center_x': 0.5, 'center_y': 0.5},'out_expo')

        else:
            quickmessage('User Error', 'There already seems to be a user assigned to this application')


    def signup_complete(self, design, instance):
        confirm = design.on_confirm()
        if confirm:
            self.signup.dismiss({'center_x': 0.5, 'center_y': -2}, 'in_expo', 0.7, 0.85, True)
            on_sucess_signup(design.ids.username.text, design.ids.password.text, design.ids.enable.active)
 
    def auth_login(self):
        result = [False, None]
        global no_user
        Logger.debug('User Status: %s', no_user)
        if no_user:
            Logger.debug('User Status: %s', no_user)
            quickmessage('User Error', 'No user was found for Reminiscor, Please [color=#00abae]Signup[/color] first.')
        else:
            try:
                print('hello')
                result = login_auth(self.ids.password.text, None)
            except Exception as e:
                Logger.debug("The exception is: %s",e)
                missing = []
                error_message = ''
                file_list = ['app_config.json', 'master_key_hash.bin', 'master_salt.bin', 'username.txt']
                for fname in os.listdir(HomeDir('', 'UserData')):
                    if fname not in file_list:
                        missing.append(fname)
                if missing:
                    error_message = 'The following file/files seem to be missing in the [color=#a93226]UserData[/color] directory:[color=#00abae]'
                    for fname in missing:
                        error_message.append('\n\u2022'+fname)
                else:
                    error_message = 'Your KeyFile has not loaded please check the directory where the [color=#a93226]KeyFile[/color] is to be found.'
                design = QuickMessage()
                app.create_popup((dp(500), dp(500)), (dp(400), dp(400)), False, design, 'Warning')
                design.ids.message.text = error_message
                design.ids.close.bind(on_release = app.close_popup)
            print('from login: ', result)
            if result[0]:
                self.ids.password.text = ''
                try:
                    with open(HomeDir('database.json', 'UserData')) as f:
                        encrypted_data =  json.load(f)
                    app.database = AES_Decrypt(result[1], encrypted_data)
                except:
                    pass
                self.transition()
            else:
                quickmessage('Login Error', 'The Master Password is [color=#a93226]wrong.[/color]')

    def transition(self, *args):
        app.root.transition = FadeTransition(duration=0.5)
        app.root.current = "main"

class Entry(RecycleDataViewBehavior, GridLayout):
    serial_no = StringProperty()
    name = StringProperty()
    url =  StringProperty()
    database_name = StringProperty()
    category = StringProperty()
    owner = ObjectProperty()

class Main(Screen):
    username = StringProperty()
    def on_enter_main(self):
        self.username = return_username()
        self.refactor_layout()
    def refactor_layout(self):
        if platform == 'android':
            self.ids.navigation_bar.remove_widget(self.ids.logo)
    def Logout(self):
        '''This function logs the user out, deletes/unassigns all decrypted data from memory'''
        # for now I am just switching screens need to rewrite this code later
        self.manager.transition = SlideTransition(direction = 'right') 
        self.manager.current = 'login'
       
class AddEntry(Screen):
    pass

class Screen_Manager(ScreenManager):
    pass

class ReminiscorApp(App):
    _platform = platform #to check the platform for sizing
    color = {'background': (30/255,30/255,30/255,1), 
             'main': (0,171/255,174/255,1), 
             'middle': (45/255,45/255,45/255,1),
             'font': (160/255,160/255,160/255,1),
             'darkgrey': (90/255,90/255,90/255,1),
             'error': (1,0,0,1)
             }
    popups = []
    animations = True # Remmeber to add an option to disable this in the settings
    database = ListProperty()
    portable = BooleanProperty(True)
    def close_popup(self, *args):
        if self.popups:
            self.popups[-1].dismiss()
            self.popups.pop(-1)

    def close_all_popups(self, *args):
        while self.popups:
            self.close_popup()
    
    def create_popup(self, max_size, min_size, multiple_allow, 
                    content, title, size_hint = (0.5,0.8), 
                    size = None, pos_hint={'center_x':0.5, 'center_y':0.5}):
        if not multiple_allow:
            self.close_all_popups() 
        popup = CustomPopup(
                        content = content,
                        title = title,
                        title_align = 'center',
                        size_hint = size_hint,
                        size_hint_max = max_size,
                        size_hint_min = min_size,
                        separator_color = self.color['main'],
                        auto_dismiss = False,
                        pos_hint = pos_hint,
                        title_font = "Fonts/Montserrat-Light.ttf",
                        background = 'UI/popup400x400.png',
                        title_color = self.color['font']
                     )
        popup.title_size = sp(20)
        if size_hint == (None, None):
            popup.size = size
        popup.open()
        self.popups.append(popup)

    def build(self):
        global app, no_user, app_path, external_path
        Logger.info('Platform: %s', self._platform)
        app=self
        if self.portable and self._platform != 'android':
            Logger.debug('Path Search: For Desktop')
            path = os.path.split(self.get_application_config())[0]
            app_path, external_path = set_app_path(self._platform, '/Reminiscor', self.portable, path)
        else:
            Logger.debug('Path Search: For Android')
            app_path, external_path = set_app_path(self._platform, '/Reminiscor', self.portable, '/sdcard')
        Logger.info('Path: %s', app_path) #/sdcard/

    def on_start(self):
        '''This function is an event to handle the start of the app, here we are going to ask for permissions'''
        if platform == 'android':
            from android.permissions import request_permissions, check_permission, Permission
            self.write_external_permission = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
            if not self.write_external_permission:
                Logger.info("Permission:%s", "Storage Permission")
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
                self.first_use()
            else:
                self.first_use()
        else:
            self.first_use()
            
    def first_use(self):
        global app, no_user, app_path, external_path
        # first we have to request a permission upon first use
        time = 0
        if platform == 'android':
            while True:
                from android.permissions import check_permission, Permission
                self.write_external_permission = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
                if self.write_external_permission:
                    break
                elif time>100000:
                    app.Exit()
                else:
                    print(time)
                    time+=1
        # here we are ensuring that the welcome screen is called and if it's a first use of the app
        no_user = not check_user()        
        if no_user:
            login_screen = app.root.get_screen('login')
            Logger.debug('Welcome is called from here the first time.')
            Clock.schedule_once(login_screen.welcome, 1)
        #self.database.append({'serial_no': '1', 'name':'Empty Database', 'url': '', 'database_name': '', 'category': 'some', 'owner': self})
if __name__ == '__main__':
    ReminiscorApp().run()