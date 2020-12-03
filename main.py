from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
#Parameters for the app
Window.clearcolor = (30/255,30/255,30/255,1)
if platform == 'win':
    print('Its Windows')
    Window.minimum_width = dp(650)
    Window.minimum_height = dp(600)

class CustomTextInput(TextInput):
    def on_parent(self, *_):
        self._refresh_text(self.text)

'''-------------------Global------------------------------'''
app = None
app_path = None
'''-------------------------------------------------------'''
'''--------------------Popups-----------------------------'''
class Signup(BoxLayout):
    pass

'''-------------------------------------------------------'''
class Login(Screen):
    def call_signup(self):
        design = Signup()
        signup = ModalView(
                            size_hint = (0.5, 0.8),
                            auto_dismiss = False,
                            size_hint_max = (dp(500),dp(600)),
                            size_hint_min = (dp(400),dp(400)),
                            background = 'UI/popup400x400.png'
                          )
        signup.add_widget(design)
        signup.open()
        design.ids.close.bind(on_release = signup.dismiss)

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

    def close_popup(self):
        if self.popups:
            self.popups[-1].dismiss()

    def close_all_popups(self):
        while self.popups:
            self.close_popups()
    
    def create_popup(self, size_hint, size, max_size, min_size, multiple_allow, content, title):
        if multiple_allow:
            self.close_all_popups() 
        popup = Popup(
                        content = content,
                        title = title,
                        size_hint = size_hint,
                        size_hint_max = max_size,
                        size_hint_min = min_size,
                        auto_dismiss = False,
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