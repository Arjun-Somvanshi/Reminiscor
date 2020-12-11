from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial
from kivy.properties import ListProperty, NumericProperty, StringProperty
from response import *
#Parameters for the app
Window.clearcolor = (30/255,30/255,30/255,1)
if platform == 'win':
    Window.minimum_width = dp(480)
    Window.minimum_height = dp(500)

'''-------------------Global------------------------------'''
app = None
app_path = None

def quickmessage(title, message, *args):
    design = QuickMessage()
    design.ids.message.text = message
    app.create_popup( (dp(400), dp(225)), (dp(400), dp(225)), True, design, title,(0.5, 0.5))
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
                self.ids.username.background_color = app.color['error']
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
    def refactor_layout(self, signup, design):
        design.ids.keyfile.remove_widget(design.ids.enable)
    def welcome(self):
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
        # binding take the tutorial button with self.tutorial, to close the window popup
        # and then activate the tutorial
        welcome_design.ids.tutorial.bind(on_release = partial(self.tutorial, welcome, False))
        welcome.open(welcome.pos_hint, {'center_x': 0.5, 'center_y': 0.5}, "out_expo")

    # This is a guided tutorial for reminiscor
    def tutorial(self, welcome, start, instance):
        global app
        if not start:    
            welcome.dismiss(self.final_dismiss_pos_hint, 'in_expo', 0.7, 0.75, True)
            welcome.bind(on_dismiss = partial(self.tutorial, welcome, True)) # This function is recurssive, depending on the value of 
            # start it decides what part of the code to execute
        if start:
            design = Tutorial()
            with open('tutorial.json') as f:
                design.text = ' '.join(json.load(f)['tutorials']['tutorial1']['content'])
            app.create_popup((dp(450),dp(550)), (dp(325), dp(400)), False, design, 'T U T O R I A L')
            design.ids.exit.bind(on_release = app.close_popup)

    # Function to invoke signup
    def call_signup(self):
        try:
            for fname in os.listdir(HomeDir('', 'UserData')):
                print(fname)
                if fname.endswith('.rem'): #if username.rem file exists then signup won't be called
                    rem_exists = True
                    break
        except:
            rem_exists = False
        if rem_exists is not True:
            design = Signup()
            self.signup = CustomModalView(
                                size_hint = (0.5, 0.8),
                                auto_dismiss = False,
                                size_hint_max = (dp(500),dp(500)),
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
            self.signup.open(self.signup.pos_hint, {'center_x': 0.5, 'center_y': 0.5},'out_expo' )
        else:
            quickmessage('User Error', 'There already seems to be a user assigned to this application')


    def signup_complete(self, design, instance):
        confirm = design.on_confirm()
        if confirm:
            self.signup.dismiss({'center_x': 0.5, 'center_y': -2}, 'in_expo', 0.7, 0.85, True)
            on_sucess_signup(design.ids.username.text, design.ids.password.text, design.ids.enable.active)

class Main(Screen):
    pass

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
    def close_popup(self, *args):
        if self.popups:
            self.popups[-1].dismiss()

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
        global app
        app = self
        app_path = os.path.split(self.get_application_config())[0]
        set_app_path(app_path)
if __name__ == '__main__':
    ReminiscorApp().run()