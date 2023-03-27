from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Color, Rectangle
from chat import ChatWindow
import json

Builder.load_file('screens/loginscreen.kv')
Builder.load_file('screens/mainscreen.kv')
Builder.load_file('screens/usercodescreen.kv')
Builder.load_file('screens/registrationscreen.kv')
Builder.load_file('screens/signupscreen.kv')
Builder.load_file('screens/qrscreen.kv')
Builder.load_file('screens/settingsscreen.kv')
# Builder.load_file('chatsscreen.kv')
Window.size = (1000, 1000)

class LoginScreen(Screen):


    def login(self, instance):

        # Check if the username and password are correct
        if self.ids.username_input.text == 'admin' and self.ids.password_input.text == 'admin123':
            # Switch to the main screen
            self.manager.current = 'main'
            self.ids.username_input.text = ''
            self.ids.password_input.text = ''
    def move_to_signup(self, instance):
        self.manager.current = 'signup'


class MainScreen(Screen):

    def switch_to_user_code_screen(self, instance):
        # Switch to the user code screen
        self.manager.transition.direction = "left"
        self.manager.current = 'user_code'
    def switch_to_registration_screen(self, instance):
        # Switch to the user code screen
        self.manager.transition.direction = "left"
        self.manager.current = 'registration'
    def switch_to_qr_screen(self, instance):
        # Switch to the user code screen
        self.manager.transition.direction = "left"
        self.manager.current = 'qr'
    def switch_to_settings_screen(self, instance):
        # Switch to settings screen
        self.manager.transition.direction = "left"
        self.manager.current = 'settings'
    def switch_to_chats_screen(self, instance):
        # Switch to chats screen
        self.manager.transition.direction = "left"
        self.manager.current = 'chats'


class UserCodeScreen(Screen):
    def verify_code(self, instance):
        code = self.ids.code_input.text
        if len(code) != 8:
            print("Code must be 8 characters long")
        elif not code.isalnum():
            print("Code must contain only letters and numbers")
        else:
        # TODO: Handle valid code
            print("Valid code entered")

class RegistrationScreen(Screen):
    def verify_code(self, instance):
        code = self.ids.code_input.text
        if len(code) != 8:
            print("Code must be 8 characters long")
class SignUpScreen(Screen):
    def switch_to_login_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'login'
class QRScreen(Screen):
    def show_qr_code(self, instance, symbol):
        self.ids.qr_code_label.text = f"QR code found"

class ChatsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        file = open("myapp/data/mock_data.json", "r")
        data = json.load(file)
        file.close()
        
        chatsPanel = TabbedPanel(do_default_tab=False,
                                 tab_pos='left_top')
        for user in data['users']['1']['conversation_to']:
            chat = ChatWindow(user, data['users']['1']['conversation_to'])
            chatsPanel.add_widget(chat)

        self.add_widget(chatsPanel)


class SettingsScreen(Screen):
    def switch_click(self, switchObject, switchValue):
        if(switchValue):
            self.ids.mail_label.text = "Powiadomienia mailowe włączone"
        else:
            self.ids.mail_label.text = "Powiadomienia mailowe wyłączone"


class MyApp(App):
    users = ["user1", "user2", "user3"]
    def build(self):

        Window.bind(on_keyboard=self.on_key)
        # Create the screen manager and add the login and main screens to it
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(QRScreen(name='qr'))
        screen_manager.add_widget(RegistrationScreen(name='registration'))
        screen_manager.add_widget(UserCodeScreen(name='user_code'))
        screen_manager.add_widget(SignUpScreen(name='signup'))
        screen_manager.add_widget(ChatsScreen(name='chats'))
        screen_manager.add_widget(SettingsScreen(name='settings'))

        return screen_manager


    def on_key(self, window, key, *args):

        if key == 27:  # 27 is the keycode for the back button
            # Switch to the previous screen
            if self.root.current == 'user_code':
                self.root.transition.direction = "right"
                self.root.current = 'main'
                return True
            elif self.root.current == 'registration':
                self.root.transition.direction = "right"
                self.root.current = 'login'
                return True
            elif self.root.current == 'chats':
                self.root.transition.direction = "right"
                self.root.current = 'main'
                return True
            elif self.root.current == 'settings':
                self.root.transition.direction = "right"
                self.root.current = 'main'
                return True
            elif self.root.current == 'qr':
                self.root.transition.direction = "right"
                self.root.current = 'main'
                return True


if __name__ == '__main__':

    MyApp().run()


