'''
Reminiscor is a free offline password manager.
Copyright (C) 2020 Arjun Somvanshi & Manvendra Somvanshi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
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
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from functools import partial
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty, BooleanProperty, OptionProperty, DictProperty
from response import * 
from kivy.logger import Logger, LOG_LEVELS
from datetime import datetime
Logger.setLevel(LOG_LEVELS["info"])
#Parameters for the app
Window.clearcolor = (30/255,30/255,30/255,1)
if platform != 'android' and 1==0:
    Window.minimum_width = dp(490)
    Window.minimum_height = dp(550)
if platform == 'win':
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
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
    app.create_popup(max_size, min_size, True, design, title,(0.5, 0.5))
    design.ids.close.bind(on_release=app.close_popup)
'''-------------------------------------------------------'''

'''-----------------Custom Classes-----------------------'''
class UIDropDownItem(Button):
    owner = ObjectProperty()
    dd_object = ObjectProperty()
    rounded = BooleanProperty(False)
    item_color = ListProperty([[1,1,1,1], [1,1,1,0.5]])
    item_font = StringProperty('Roboto')
    item_font_size = NumericProperty(sp(15))
    item_font_color = ListProperty([0,0,0,1])
    background_img_normal = StringProperty('')
    background_img_down = StringProperty('')
    def on_release(self):
        self.owner.selected_item = self.text
        self.dd_object.dropdown_view.dismiss()

class UIDropDownContent(BoxLayout):
    Elements = ListProperty([]) 
    selected_item = StringProperty('')
    background_color = ListProperty([0,0,0,1])
    item_height = NumericProperty(dp(30))
    item_size_hint_x = NumericProperty(1)
    def __init__(self, dropdown_instance, elements: list, background_color: list, item_height = dp(30), **kwargs):
        super(UIDropDownContent, self).__init__(**kwargs)
        for element in elements:
            self.Elements.append({'text': element, 
                                  'owner': self, 
                                  'dd_object': dropdown_instance, 
                                  'item_color': dropdown_instance.dd_item_color,
                                  'background_img_down': dropdown_instance.dd_item_img_down,
                                  'background_img_normal': dropdown_instance.dd_item_img_normal,
                                  'rounded': dropdown_instance.dd_item_isrounded,
                                  'pos_hint': {'center_x': 0.5}, # this is how you would center widgets inside a recycle view
                                  'item_font': dropdown_instance.dd_item_font,
                                  'item_font_color': dropdown_instance.dd_item_font_color,
                                  'item_font_size': dropdown_instance.dd_item_font_size
                                  })
            self.background_color = background_color
            self.item_height = item_height
            self.item_size_hint_x = dropdown_instance.dd_item_size_hint_x

class UIDropDown(Button):
    dd_open_vertical = OptionProperty('down', options = ['up', 'down', 'win_center'])
    dd_open_horizontal = OptionProperty('center', options = ['left', 'center', 'right', 'win_center'])
    def calculate_minimum_height(self):
        required_height = 0
        for i in range(self.show_items):
            required_height += self.dd_item_height + dp(15)
        return required_height + dp(15)
    
    def __init__(self, **kwargs):
        self.register_event_type('on_set')
        super(UIDropDown, self).__init__(**kwargs)
    
    def on_set(self):
        pass

    def set_dropdown(self):
        self.content = UIDropDownContent(self, self.elements, self.dd_background_color, self.dd_item_height)
        if self.calculate_ddheight:
            self.dd_size[1] = self.calculate_minimum_height()
        self.dropdown_view = DropDownModalView(
                                           size_hint = (None, None),
                                           size = self.dd_size,
                                           overlay_color = (0,0,0,0)
                                       )
        if self.dd_open_vertical == 'down':
            vertical =  ['top',self.y/Window.height]
        elif self.dd_open_vertical == 'up':
            vertical = ['y', self.top/Window.height]
        if self.dd_open_horizontal == 'center':
            horizontal = ['center_x', self.center_x/Window.width]
        elif self.dd_open_horizontal == 'left':
            horizontal  = ['x', self.x/Window.width]
        elif self.dd_open_horizontal == 'right':
            horizontal = ['right', self.right/Window.width]
        if self.dd_open_vertical == 'win_center' or self.dd_open_horizontal == 'win_center':
            horizontal = ['center_x', 0.5]
            vertical = ['center_y', 0.5]
        self.dropdown_view.pos_hint = {horizontal[0]: horizontal[1], vertical[0]: vertical[1]}
        self.dropdown_view.add_widget(self.content)
        self.dropdown_view.bind(on_dismiss = self.set_selected_item)
        Window.bind(on_resize=partial(self.dropdown_view.dismiss, True))
    
    def on_release(self):
        self.set_dropdown()
        self.dropdown_view.open(self.dd_size[1])

    def set_selected_item(self, instance):
        if self.content.selected_item:
            self.text = self.content.selected_item
        self.dispatch('on_set')

class CustomTextInput(TextInput):
    def on_parent(self, *_):
        self._refresh_text(self.text)

class EntryTextInput(TextInput):
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

class DropDownModalView(ModalView):
    def open(self, final_height, *largs, **kwargs):
        self.height = 0
        self.opacity = 0
        anim = Animation(height = final_height, t = 'in_expo', duration = 0.4)
        anim &= Animation(opacity=1, t='in_expo', duration = 0.4)
        anim.start(self)
        super(DropDownModalView, self).open(*largs, **kwargs)
    
    def dismiss(self, fast = False, *largs, **kwargs):
        if not fast:
            anim = Animation(height = 0, t='out_expo', duration=0.4)
            anim &= Animation(opacity = 0, t='out_expo', duration=0.4)
            anim.start(self)
            anim.bind(on_complete = self.finish_dismiss)
        else:
            super(DropDownModalView, self).dismiss()
    
    def finish_dismiss(self, *args):
        super(DropDownModalView, self).dismiss()

class Scaffold(GridLayout):
    pass

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
        result = api.signup_response(self.ids.username.text, self.ids.password.text, self.ids.c_password.text)
        if 0 in result:
            if result[0] == 0: # meaning the username is less than 3 chars
                self.ids.username.error = True
                quickmessage('Username Error', "Your username should be atleast 3 characters long")
            elif result[1] == 0: # password less than 8
                self.ids.username.error = False
                self.ids.password.error = True
                quickmessage('Master Password Error', "Your password should be atleast 8 characters long")
            elif result[2] == 0: # password do not match
                self.ids.username.error = False
                self.ids.password.error = True
                self.ids.c_password.error  = True
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

class NavigationView(BoxLayout):
    def on_touch_down(self, touch):
        global app
        if not (touch.x > self.x and touch.x<self.right and touch.y > self.y and touch.y<self.top):
            app.nav.dismiss({'right': 2, 'center_y': 0.5}, 'linear', 0.5, 0.55)
        super(NavigationView, self).on_touch_down(touch)

class NewCategory(BoxLayout):
    def add_category(self):
        global app
        # check if category already exists for given database
        if api.isalnum_with_space(self.ids.category.text):
            if api.add_category(self.ids.database_dropdown.text, self.ids.category.text, app.master_key):
                app.categories = api.return_category_keys(self.ids.database_dropdown.text, app.master_key)
                app.close_popup()
                quickmessage("Succes", "Category Added.")
            else:
                quickmessage("Category Error", "This category already exists in database.")
        else:
            quickmessage("Category Error", "The category name should be alpha-numeric.")

class NewDatabase(BoxLayout):
    def add_database(self):
        global app
        # check if category already exists for given database
        if api.isalnum_with_space(self.ids.database.text):
            if api.add_database(self.ids.database.text, app.master_key):
                app.databases = api.return_database_keys(app.master_key)
                app.close_popup()
                quickmessage("Succes", "Database Added.")
            else:
                quickmessage("Database Error", "This database already exists.")
        else:
            quickmessage("Database Error", "The database name should be alpha-numeric.")

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
        Logger.info('Welcome was called')
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
        rem_exists = api.check_user()
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
            Logger.info('Signup was called here')
            self.signup.open(self.signup.pos_hint, {'center_x': 0.5, 'center_y': 0.5},'out_expo')

        else:
            quickmessage('User Error', 'There already seems to be a user assigned to this application')


    def signup_complete(self, design, instance):
        confirm = design.on_confirm()
        if confirm:
            design.ids.username.error = False
            design.ids.password.error = False
            design.ids.c_password.error  = False
            self.signup.dismiss({'center_x': 0.5, 'center_y': -2}, 'in_expo', 0.7, 0.85, True)
            api.on_success_signup(design.ids.username.text, design.ids.password.text, design.ids.enable.active)
            try:
                Logger.info("User created %s", "Fetching username.")
                global app
                app.username = return_username()
            except Exception as e:
                Logger.info("User Error %s", str(e))


 
    def auth_login(self):
        result = [False, None]
        global no_user, app
        Logger.info('User Status: %s', no_user)
        if no_user:
            Logger.info('User Status: %s', no_user)
            quickmessage('User Error', 'No user was found for Reminiscor, Please [color=#00abae]Signup[/color] first.')
        else:
            try:
                Logger.info("User Login %s", "User exists, authentication is being done...")
                result = api.auth_login(self.ids.password.text, None)
            except Exception as e:
                Logger.info("The exception is: %s",e)
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
            if result[0]:
                self.ids.password.text = ''
                self.ids.password.error = False
                self.transition()
                #self.start_session(result[1])
                app.master_key = result[1]
                # unassigning the derived master key from the result
                result = [1,2,''] # random reassignment of the list 
                app.databases = api.return_database_keys(app.master_key)
                mainscreen = app.root.get_screen("main") 
                mainscreen.loadview()
            else:
                self.ids.password.error = True

    def transition(self, *args):
        app.root.transition = FadeTransition(duration=0.5)
        app.root.current = "main"

class Entry(RecycleDataViewBehavior, GridLayout):
    title = StringProperty('')
    sensitive_data = DictProperty({})
    random_key = StringProperty('')
    time = StringProperty('')

class Main(Screen):
    first_entry = BooleanProperty(True)
    loaded_database = StringProperty("Database [main]")
    def on_enter_main(self):
        self.refactor_layout()
    def refactor_layout(self):
        if platform == "android":
           self.ids.scaffold.remove_widget(self.ids.scaffold.ids.logo)
    def search_limit(self):
        '''This limits the search bars characters from exeding 32'''
        if len(self.ids.search_bar.text) > 32:
            self.ids.search_bar.text = self.ids.search_bar.text[:-1]
    def loadview(self):
        global app
        if checkfile("database.remdb"):
            if self.first_entry:
                app.database = api.decrypt_database(app.master_key)["Database [main]"]
                app.categories = ['Category'] + api.return_category_keys("Database [main]", app.master_key)
                self.first_entry = False
            else:
                if self.ids.category.text == 'Category':
                    app.database = api.decrypt_database(app.master_key)[self.ids.database.text]
                else:
                    app.database = api.decrypt_database(app.master_key)[self.ids.database.text + '_categories'][self.ids.category.text]
                app.categories = ['Category'] + api.return_category_keys(self.ids.database.text, app.master_key)

    def on_pre_enter(self):
        if app.master_key != None:
            self.loadview()
    def set_database_and_load_categories(self, database_name):
        global app
        if database_name != self.loaded_database:
            app.database = api.decrypt_database(app.master_key)[database_name]
            app.categories = ['Category'] + api.return_category_keys(database_name, app.master_key)
            self.loaded_database = database_name
            self.ids.category.text = 'Category'
    
    def show_category(self, category):
        if category != "Category":
            app.database = api.decrypt_database(app.master_key)[self.ids.database.text + '_categories'][category]
        else:
            app.database = api.decrypt_database(app.master_key)[self.ids.database.text]
        
class AddEntry(Screen):
    passwordChanged = NumericProperty(0)
    titleChanged = NumericProperty(0)
    def on_enter(self):
        self.ids.password.bind(focus=self.monitor_password)
        self.ids.title.bind(focus=self.monitor_titleInput_length)
    def reset_text_input(self, textinput):
        textinput.text = ''
        textinput.error = False
    def reset_screen_attrs(self, *args):
        # reset the text inputs
        self.reset_text_input(self.ids.title)
        self.reset_text_input(self.ids.url)
        self.reset_text_input(self.ids.username)
        self.reset_text_input(self.ids.password)
        self.reset_text_input(self.ids.notes)
        # reset the drop downs 
        self.ids.category_dropdown.text = 'Default'
        self.ids.category_dropdown.error = False
        self.ids.database_dropdown.text = 'Database [main]'
        self.ids.database_dropdown.error = False
        # reset the message
        self.ids.message.text = ""
    def back(self):
        # change screen
        self.manager.transition = SlideTransition(direction="down")
        self.manager.current = "main"
        # reset the screen attributes
        # scheduling so that the attributes change after screen switching animation is completed
        Clock.schedule_once(self.reset_screen_attrs, 0.1)
    def monitor_titleInput_limit(self):
        # for checking if number of characters exceeded 32
        if len(self.ids.title.text) > 32:
            self.ids.title.text = self.ids.title.text[:-1]
    def monitor_titleInput_length(self, title, value):
        if self.titleChanged == 0:
            self.titleChanged = 1
        if value == False and len(title.text)<3:
            title.error = True
            self.ids.message.text = "Enter a title of atleast [color=#770000]3 characters."
        elif value == False and len(title.text)>=3:
            title.error = False
            self.ids.message.text = ""
            #if self.passwordChanged == 1 and len(self.ids.password.text)<8:
                #self.monitor_password(self.ids.password, False)
    def monitor_password(self, password, value):
        if self.passwordChanged == 0:
            self.passwordChanged = 1
        if value == False and len(password.text)<8:
            password.error = True
            self.ids.message.text = "Enter a password of atleast [color=#770000]8 characters."
        elif value == False and len(password.text)>=8:
            password.error = False
            self.ids.message.text = ""
            if self.titleChanged and len(self.ids.title.text)<3:
               self.monitor_titleInput_length(self.ids.title, False)

    def identify_errors(self):
        if len(self.ids.title.text)>=3:
            if api.isalnum_with_space(self.ids.title.text):
                if len(self.ids.password.text)>=8:
                    self.ids.message.text = ""
                    return False 
                else:
                    self.ids.message.text = "Enter a password of atleast [color=#770000]8 characters." 
                    self.ids.password.error = True
                    return True 
            else:
                self.ids.message.text = "Enter a title that is [color=#770000]alpha numeric."
                self.ids.title.error = True
                return True 
        else:
            self.ids.message.text = "Enter a title of atleast [color=#770000]3 characters."
            self.ids.title.error = True
            return True 

    def load_categories(self, database_name):
        global app
        app.categories = api.return_category_keys(database_name, app.master_key)
        self.ids.category_dropdown.text = "Default"
         
    def add_entry(self):
        if not self.identify_errors():
            database_name = self.ids.database_dropdown.text
            category = self.ids.category_dropdown.text
            time_now = datetime.now()
            time = time_now.strftime("%B %d, %Y@%H:%M:%S")
            # Now we must secure the sensitive data  
            sensitive_data = {"url": self.ids.url.text, "username": self.ids.username.text, 
                              "password": self.ids.password.text, "notes": self.ids.notes.text}
            encrypted_sensitive_data, random_key = api.sensitive_data_encrypt(sensitive_data)
            entry = {"title": self.ids.title.text, "sensitive_data": encrypted_sensitive_data, 
                     "random_key": str(random_key), "time": time}
            print(category)
            api.add_entry(database_name, category, app.master_key, entry)
            quickmessage("Success", "The entry was added to database.")
            self.reset_screen_attrs()

    def new_category(self):
        global app
        content = NewCategory()
        app.create_popup([dp(600),dp(400)], [dp(400),dp(400)], False, content, 'Add Category')

    def new_database(self):
        global app
        content = NewDatabase()
        app.create_popup([dp(400),dp(300)], [dp(400),dp(400)], False, content, 'Add Database')


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
    database = ListProperty([]) # The database to be used for recycle view on entry view screen
    databases = ListProperty([]) # list of all the names of different databases
    categories = ListProperty([])
    portable = BooleanProperty(True)
    username = StringProperty()
    master_key = None 

    def navigation(self):
        nav_content = NavigationView() 
        self.nav = CustomModalView(
                            size_hint = (0.5, 1),
                            size_hint_max = (dp(250), None),
                            size_hint_min = (dp(100), None),
                            background = 'UI/popup400x400.png',
                            auto_dismiss = False,
                            overlay_color= (0,0,0,0.5),
                            opacity = 0, 
                            pos_hint = {'right': 2, 'center_y': 0.5}
                        )
        self.nav.add_widget(nav_content)
        self.nav.open({'right':2, 'center_y': 0.5}, {'right': 1, 'center_y': 0.5}, 'linear', 0.5, 0.55)
    
    def logout(self):
        '''This function logs the user out, deletes/unassigns all decrypted data from memory'''
        # for now I am just switching screens need to rewrite this code later
        app.root.transition = SlideTransition(direction = 'right') 
        app.root.current = 'login'

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
        if self._platform != 'android':
            Logger.info('Path Search: For Desktop')
            if self.portable:
                Logger.info('Mode: Portable')
                path = os.path.split(self.get_application_config())[0]
                Logger.info("application config path: %s", path)
                path_as_list= path.split(os.path.sep)
                path_as_list.pop(-1)
                path = os.path.sep.join(path_as_list) 
                app_path, external_path = set_app_path(self._platform, 'Reminiscor', self.portable, path)
            else:
                Logger.info('Mode: Install')
                app_path, external_path = set_app_path(self._platform, 'Reminiscor', self.portable)
        else:
            Logger.info('Path Search: For Android')
            app_path, external_path = set_app_path(self._platform, '/Reminiscor', self.portable, '/sdcard')
        Logger.info('Set Path: %s', app_path) #/sdcard/
        # get the username for the app session
        try:
            self.username = return_username()
        except Exception as e:
            Logger.info("User Error: %s", str(e))

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
                elif time>20000:
                    app.Exit()
                else:
                    print(time)
                    time+=1
        # here we are ensuring that the welcome screen is called and if it's a first use of the app
        no_user = not api.check_user()        
        if no_user:
            login_screen = app.root.get_screen('login')
            Logger.info('Welcome is called from here the first time.')
            Clock.schedule_once(login_screen.welcome, 1)
if __name__ == '__main__':
    ReminiscorApp().run()
