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
from FileHandling import *
#Parameters for the app
Window.clearcolor = (30/255,30/255,30/255,1)
if platform == 'win':
    Window.minimum_width = dp(480)
    Window.minimum_height = dp(500)
'''-----------------Custom Classes-----------------------'''
class CustomTextInput(TextInput):
    def on_parent(self, *_):
        self._refresh_text(self.text)

class CustomModalView(ModalView):

    def open(self, pos_hint_initial = {}, pos_hint_final = {}, 
             t = '', d1=0.7, d2=1.5, animate = True, *largs, **kwargs):
        global app
        #print(app.animations)
        if animate and app.animations:
            #print('animating')
            self.pos_hint = pos_hint_initial
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 1, t=t, duration=d2)
            anim.start(self)
        else: 
            self.opacity = 1
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        super(CustomModalView, self).open(*largs, **kwargs)

    def dismiss(self, pos_hint_final = {}, t = '', d1=0.7, d2=0.75, animate = True, *largs, **kwargs):
        #print('dismissing')
        self.disabled = True
        if animate and app.animations:
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 0, t=t, duration = d2)
            anim.start(self)
            anim.bind(on_complete = self.finish_dismiss)
        else:
            super(CustomModalView, self).dismiss()

    def finish_dismiss(self, *args):
        super(CustomModalView, self).dismiss()
'''------------------------------------------------------'''
'''-------------------Global------------------------------'''
app = None
app_path = None
'''-------------------------------------------------------'''
'''--------------------Popups-----------------------------'''
class Signup(BoxLayout):
    pass
class Welcome(BoxLayout):
    text = StringProperty('')
    def __init__(self, **kwargs):
        super(Welcome, self).__init__(**kwargs)
        file = open('welcome.txt', 'r')
        self.text = '\n'.join(ReadFile(file))

'''-------------------------------------------------------'''
class Login(Screen):
    def tutorial(self):
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
        final_dismiss_pos_hint = {'center_x': -2, 'center_y':0.5 }
        welcome_design.ids.close.bind(on_release= partial(welcome.dismiss,final_dismiss_pos_hint, 'in_expo', 0.7, 0.75, True))
        welcome.open(welcome.pos_hint, {'center_x': 0.5, 'center_y': 0.5}, "out_expo")
    
    # Function to invoke signup
    def call_signup(self):
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
        final_pos_hint = {'center_x': 0.5, 'center_y': -2}
        design.ids.close.bind(on_release = partial(self.signup.dismiss, final_pos_hint,'in_expo', 0.7, 0.85, True))
        self.signup.open(self.signup.pos_hint, {'center_x': 0.5, 'center_y': 0.5},'out_expo' )

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
             'font': (140/255,140/255,140/255,1),
             'darkgrey': (90/255,90/255,90/255,1)
             }
    popups = []
    animations = True # Remmeber to add an option to disable this in the settings
    def close_popup(self):
        if self.popups:
            self.popups[-1].dismiss()

    def close_all_popups(self):
        while self.popups:
            self.close_popups()
    
    def create_popup(self, max_size, min_size, multiple_allow, 
                    content, title, size_hint = (0.5,0.8), 
                    size = None, pos_hint={'center_x':0.5, 'center_y':0.5}):
        if multiple_allow:
            self.close_all_popups() 
        popup = Popup(
                        content = content,
                        title = title,
                        size_hint = size_hint,
                        size_hint_max = max_size,
                        size_hint_min = min_size,
                        auto_dismiss = False,
                        pos_hint = pos_hint
                     )
        if size_hint == (None, None):
            popup.size = size
        popup.open()
        self.popups.append(popup)

    def build(self):
        global app
        app = self
if __name__ == '__main__':
    ReminiscorApp().run()