from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty
import time
from functools import partial
kv = '''
Screen_Manager:
    Main
    Side
<Main>:
    name: 'main'
    BoxLayout:
        padding: 100
        Button: 
            text: 'enter'
            on_release: root.pop()
<Side>:
    on_enter: root.decrypt_database()
    name: 'side'
    BoxLayout:
        padding: 100
        Button: 
            text: 'exit'
            on_release:
                root.transition()
<pop>:
    ProgressBar:
        id: prog
        value: 0
'''
class pop(BoxLayout):
    pass
class Main(Screen):
    def pop(self):
        self.design = pop()
        self.win = Popup(title = 'Hello', content=self.design, size_hint = (None, None), size = (400,400), auto_dismiss=False)
        self.win.open()
        Clock.schedule_once(self.transition, 1)
    def transition(self, *args):
        app = App.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'side'
class Side(Screen):
    def decrypt_database(self):
        self.main = self.manager.get_screen('main')
        time = 0.5
        value = 25
        for i in range(4):
            print('this is the time: ', time)
            Clock.schedule_once(partial(self.increment_value, value), time)
            value += 25
            time+=0.5
            if value==100:
                Clock.schedule_once(self.diss, 2)
    def diss(self,*args):
        self.main.win.dismiss()
    def increment_value(self, value, *args):
        self.main.design.ids.prog.value = value
        print('this is the value: ', value)

    def transition(self):
        app = App.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'main'
class Screen_Manager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    MyApp().run()