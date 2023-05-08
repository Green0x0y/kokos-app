import base64
import time
import tempfile
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Color, Rectangle
from chat import ChatWindow
from kivy_garden.zbarcam import ZBarCam
from login import LoginScreen
from signup import SignUpScreen
from data.AuthService import AuthService
from data.DataProvider import DataProvider
from PIL import Image
# import json
import firebase
import qrcode
from io import BytesIO

# from firebase_admin import credentials, db
# cred = credentials.Certificate('data/kokos-dd14a-firebase-adminsdk-dnceg-c713762a6a.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://kokos-dd14a-default-rtdb.firebaseio.com/'
# })

config = {
    "apiKey": "AIzaSyCuFVfP62CtZdUCokK8mdjhof-FZbHkf2M",
    "authDomain": "kokos-dd14a.firebaseapp.com",
    "databaseURL": "https://kokos-dd14a-default-rtdb.firebaseio.com/",
    "projectId": "kokos-dd14a",
    "storageBucket": "kokos-dd14a.appspot.com",
    "messagingSenderId": "517554075184",
    "appId": "appId"
}

app = firebase.initialize_app(config)
auth_service = AuthService(app)
data_provider = DataProvider(app, auth_service=auth_service)

Builder.load_file('screens/loginscreen.kv')
Builder.load_file('screens/mainscreen.kv')
Builder.load_file('screens/usercodescreen.kv')  
Builder.load_file('screens/registrationscreen.kv')
Builder.load_file('screens/signupscreen.kv')
Builder.load_file('screens/qrscreen.kv')
Builder.load_file('screens/settingsscreen.kv')
Builder.load_file('screens/adddamagescreen.kv')
Builder.load_file('screens/yourqrcodescreen.kv')
Window.size = (500, 700)


class MainScreen(Screen):
    # user_data = self.db.get_user_data(auth_service.user['localId']).get()
    def __init__(self, data_provider: DataProvider, **kw):
        super().__init__(**kw)
        
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

    def on_enter(self):
        label = self.ids.username
        if auth_service.user is None:
            label.text = " unresgistered"
        label.text = "Cześć " + data_provider.get_current_user_data()['username'] + "!"

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
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def find_user_by_registration(self, registration):
        # ref = db.reference("users")
        # users = ref.get()
        # registration = self.ids.code_input.text
        # if users is not None:
        #     for username, user in users.items():
        #         if registration in user.get("registrations", []):
        #             return username
        users = self.db.get_users().get()
        for user in users.each():
            user_data = self.db.get_user_data(user.key()).child('registrations').get().val()
            print(user_data)
            if user_data is not None and registration in user_data:
                 return user.key(), ""
        else:
            return None, ""

    def go_to_chat(self, instance):
        registration = self.ids.code_input.text
        error_label = self.ids["error_label"]
        error_label.text = ""
        if len(registration) != 8:
            error_label.text = "Nieprawidłowa dłogość"
        userId, error = self.find_user_by_registration(registration)
        error_label.text = error

        if not userId:
            error_label.text = "Nie ma takiej rejestracji"
        else:
            self.manager.transition.args = {'receiver_id': userId, 'registration': registration}
            self.manager.current = 'damage'
            error_label.text = ""


class QRScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
    def find_user_by_qr(self, qr_data):
        users = self.db.get_users().get()
        for user in users.each():
            user_qr_code = self.db.get_user_data(user.key()).child('qr_code').get().val()

            if user_qr_code is not None and qr_data == user_qr_code:
                print("kod" ,user_qr_code)
                return user.key(), ""
        else:
            return None, ""


    def switch_to_damage(self, instance, *args):
        symbol = instance.symbols[-1]  # Ostatni zeskanowany symbol
        qr_data = symbol.data.decode('utf-8')
        print(qr_data)
        userId, error = self.find_user_by_qr(qr_data)
        self.ids.qr_code_label.text = error

        if not userId:
            self.ids.qr_code_label.text = "Nie ma takiego kodu"
        else:
            self.manager.transition.args = {'receiver_id': userId, 'registration': 'Wczytano QR'}
            self.manager.current = 'damage'
            self.ids.qr_code_label.text  = ""


class ChatsScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def on_enter(self, *args):
        conversations = self.db.get_conversations(self.auth.get_uid())
        chatsPanel = TabbedPanel(do_default_tab=False, tab_pos='left_top')

        if len(conversations) != 0:
            for key in conversations:
                other_user = self.db.get_other_uid(self.auth.get_uid(), key)
                if conversations[key] is not None:
                    chat = ChatWindow(self.db, self.auth, other_user, conversations[key])
                    chatsPanel.add_widget(chat)
        self.add_widget(chatsPanel)


class SettingsScreen(Screen):
    def switch_click(self, switchObject, switchValue):
        if (switchValue):
            self.ids.mail_label.text = "Powiadomienia mailowe włączone"
        else:
            self.ids.mail_label.text = "Powiadomienia mailowe wyłączone"
    def switch_to_my_qr_code(self, instance):
        self.manager.current = 'yourqrcode'

class YourQrCodeScreen(Screen):

    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
    def on_enter(self, *args):
        qr_data = data_provider.get_current_user_data()['qr_code'];
        qr = qrcode.QRCode(version=1, box_size=20, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert PIL Image to RGBA and then to base64
        img_rgba = img.convert('RGBA')
        buffered = BytesIO()
        img_rgba.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Update the source of the Image widget to display the QR code
        self.ids.qr_code_image.source = f'data:image/png;base64,{img_str}'
        self.ids.qr_code_image.reload()


class AddDamageScreen(Screen):
    def __init__(self, db,  **kw):
        super().__init__(**kw)
        self.db = db
        self.receiver_id = None
        self.registration = None

    def on_enter(self, *args):
        self.receiver_id = self.manager.transition.args.get('receiver_id')
        self.registration = self.manager.transition.args.get('registration')
        if self.receiver_id:
            rounded_input = self.ids.registration
            rounded_input.text = self.registration

    def send(self):
        message = self.ids.message.text
        if message == "":
            return
        # self.manager.transition.args = {'message': message}
        # self.db.add_message(message, auth_service.user['localId'], self.receiver_id)\
        self.db.add_conversation(message, auth_service.user['localId'], self.receiver_id)
        self.ids.message.text = ''
        self.ids.result.text = 'Wiadomość wysłana!'
        self.manager.transition.args = {"to" : self.receiver_id}
        self.manager.current = 'chats'



class MyApp(App):

    def build(self):
        Window.bind(on_keyboard=self.on_key)
        # Create the screen manager and add the login and main screens to it
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(auth_service, data_provider, name='login'))
        screen_manager.add_widget(MainScreen(data_provider, name='main'))
        screen_manager.add_widget(QRScreen(auth_service, data_provider, name='qr'))
        screen_manager.add_widget(RegistrationScreen(auth_service, data_provider, name='registration'))
        screen_manager.add_widget(UserCodeScreen(name='user_code'))
        screen_manager.add_widget(SignUpScreen(auth_service, data_provider, name='signup'))
        screen_manager.add_widget(ChatsScreen(auth_service, data_provider, name='chats'))
        screen_manager.add_widget(SettingsScreen(name='settings'))
        screen_manager.add_widget(AddDamageScreen(data_provider, name='damage'))
        screen_manager.add_widget(YourQrCodeScreen(auth_service, data_provider, name='yourqrcode'))

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
            elif self.root.current == 'yourqrcode':
                self.root.transition.direciton = "right"
                self.root.current = 'settings'
                return True


if __name__ == '__main__':
    MyApp().run()


