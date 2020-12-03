from kivy.app import App
from kivy.lang import Builder

KV='''
BoxLayout:
    canvas.before:
        Color:
            rgba: (1,0,0,1)
        Rectangle:
            pos: self.pos
            size: self.size
    padding: 20
    BoxLayout:
        pos_hint: {'top': 0.8}
        canvas.before:
            Color:
                rgba: (0,0,1,1)
            Rectangle:
                pos: self.pos
                size: self.size
        padding: 100
        spacing: 20
        orientation: 'vertical'
        Button:
            text: 'hello'
        BoxLayout:
            pos_hint: {'x': 0.1}
            Button:
                text: 'b1'
            Button:
                text: 'b2'
        Button:
            text: 'end'
'''

class MyApp(App):
    def build(self):
        return Builder.load_string(KV)
if __name__ == '__main__':
    MyApp().run()