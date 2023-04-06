from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Color, Rectangle
from chat import ChatWindow
from kivy_garden.zbarcam import ZBarCam
import json
import firebase_admin

from firebase_admin import credentials, db
cred = credentials.Certificate('data/kokos-dd14a-firebase-adminsdk-dnceg-c713762a6a.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kokos-dd14a-default-rtdb.firebaseio.com/'
})
ref = db.reference('users')


Builder.load_file('screens/loginscreen.kv')
Builder.load_file('screens/mainscreen.kv')
Builder.load_file('screens/usercodescreen.kv')
Builder.load_file('screens/registrationscreen.kv')
Builder.load_file('screens/signupscreen.kv')
Builder.load_file('screens/qrscreen.kv')
Builder.load_file('screens/settingsscreen.kv')
Builder.load_file('screens/adddamagescreen.kv')
Window.size = (600, 600)


class LoginScreen(Screen):
    def validate_user(self, username, password):

        user_ref = ref.child(username)
        user_data = user_ref.get()
        if user_data is None:
            return False, 'Użytkownik o podanej nazwie nie istnieje'
        if password != user_data.get('password'):
            return False, 'Nieprawidłowe hasło'
        return True, user_data
    def login(self, instance):
        # Check if the username and password are correct
        username_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        success, data = self.validate_user(username_input, password_input)
        if success:
            print('Zalogowano!')
            self.manager.current = 'main'
        else:
            print(f'Błąd logowania: {data}')


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
        else:
            self.manager.current = 'damage'


class SignUpScreen(Screen):
    ref = db.reference('users')
    def check_passwords(self, password, password2):
        return password == password2

    def check_valid_email(self, email):
        return '@' in email
    def check_user_exists(self, email, username):

        users = ref.get()
        if users is not None:
            for user in users.values():
                if user.get('email') == email or user.get('username') == username:
                    return True
    def switch_to_login_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'login'
    def add_user(self, instance):
        username_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        email_input = self.ids.email_input.text
        password_input_2 = self.ids.password_input_2.text



        if self.check_user_exists(email_input, username_input):
            print("email lub login istnieje")
        elif not self.check_valid_email(email_input):
            print("nieprawidłowy mail")
        elif not self.check_passwords(password_input, password_input_2):
            # wyprintuj błąd na polu
            print("zle hasla")
        else:
            user_data = {
                'id': len(ref.get()) + 1,
                'password': password_input,
                'qr_code': '',
                'email': email_input
            }
            ref.child(username_input).set(user_data)
            self.switch_to_login_screen();
            print("logowanie")





class QRScreen(Screen):
    def show_qr_code(self, instance, symbol):
        self.ids.qr_code_label.text = f"QR code found"
    def switch_to_damage(self, instance):
        self.manager.current = 'damage'

class ChatsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        file = open("data/mock_data.json", "r")
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
        if (switchValue):
            self.ids.mail_label.text = "Powiadomienia mailowe włączone"
        else:
            self.ids.mail_label.text = "Powiadomienia mailowe wyłączone"


class AddDamageScreen(Screen):
    pass


class MyApp(App):


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
        screen_manager.add_widget(AddDamageScreen(name='damage'))

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
                self.root.current = 'main'
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
            elif self.root.current == 'signup':
                self.root.transition.direction = "left"
                self.root.current = 'login'
                return True
            elif self.root.current == 'damage':
                self.root.transition.direction = "right"
                self.root.current = 'main'
                return True


if __name__ == '__main__':
    MyApp().run()


