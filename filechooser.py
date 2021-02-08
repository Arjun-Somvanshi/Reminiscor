from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.properties import StringProperty
import os

kv = '''

'''

class FilePicker(BoxLayout):
    default_path = StringProperty('')
    def set_default_path(self):
        if platform == "win":
            os.expanduser(path)