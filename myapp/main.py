import base64
import smtplib
import time
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Color, Rectangle
from kivy.uix.togglebutton import ToggleButton

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
# Builder.load_file('screens/qrscreen.kv')
Builder.load_file('screens/settingsscreen.kv')
Builder.load_file('screens/adddamagescreen.kv')
Builder.load_file('screens/yourqrcodescreen.kv')
Builder.load_file('screens/addregistrationscreen.kv')
Builder.load_file('screens/deleteregistrationscreen.kv')
Builder.load_file('screens/updateusernamescreen.kv')
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
    def switch_to_my_qr_code(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = 'yourqrcode'

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
        if len(registration) != 7:
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
        self.initiated = False
# to jest zdecydowanie do zrefactorowania, ale for now działa
    def on_enter(self, *args):

        def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size
        
        if self.initiated: return
        conversation_IDs = self.db.get_conversations_IDs(self.auth.get_uid())
        chatsPanel = TabbedPanel(do_default_tab=False, tab_pos='left_mid')

        with chatsPanel.canvas.before:
            Color(133/255, 106/255, 85/255, 1) # brown
            chatsPanel.rect = Rectangle(pos=chatsPanel.pos, size=chatsPanel.size)
        chatsPanel.bind(pos=update_rect, size=update_rect)

        if len(conversation_IDs) != 0:
            first_tab = True
            for conv in conversation_IDs:
                chat = ChatWindow(self.db, self.auth, conv)
                chatsPanel.add_widget(chat)
                if first_tab:
                    chat.on_press()
                    chatsPanel.set_def_tab = chat
                    first_tab = False

        self.add_widget(chatsPanel)
        self.initiated = True


class SettingsScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def switch_click(self, switchObject, switchValue):
        if (switchValue):
            self.ids.mail_label.text = "Powiadomienia mailowe włączone"
        else:
            self.ids.mail_label.text = "Powiadomienia mailowe wyłączone"

    def switch_to_addregistration_screen(self, instance):
        # Switch to chats screen
        self.manager.transition.direction = "left"
        self.manager.current = 'addregistration'

    def switch_to_deleteregistration_screen(self, instance):
        # Switch to chats screen
        self.manager.transition.direction = "left"
        self.manager.current = 'deleteregistration'
    def switch_to_updateusername_screen(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = 'updateusername'


class UpdateUsernameScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
    def on_enter(self):
        current_username = self.ids["current_username"]
        current_username.text = self.db.get_username(self.auth.user['localId'])
    def update(self):
        self.db.update_username(self.auth.user['localId'],  self.ids["code_input"].text)
        success_label = self.ids["success_label"]
        success_label.text = "Pomyślnie zmieniono"
        self.on_enter()


    def on_leave(self):
        success_label = self.ids["success_label"]
        success_label.text = ""
        self.ids["code_input"].text = ""
class AddRegistrationScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
    def on_enter(self):
        print("entered add registration")
    def check_registration_exists(self, new_registration):
        users = self.db.get_users().get()
        for user in users.each():
            user_registrations = self.db.get_user_registrations(user.key())
            # if there is the same registration
            if user_registrations is not None and new_registration  in user_registrations:
                return True, "Taka rejestracja już istnieje"
        else:
            return False, ""

    def add_registration(self, instance):
        success_label = self.ids["success_label"]
        success_label.text = ""
        userId = self.auth.user['localId']
        new_registration = self.ids.code_input.text
        error_label = self.ids["error_label"]
        error_label.text = ""
        if len(new_registration) != 7:
            error_label.text = "Nieprawidłowa dłogość"
        exists, error = self.check_registration_exists(new_registration)
        error_label.text = error
        if not exists:
            self.db.add_registration_db(userId, new_registration)
            success_label.text = "Pomyślnie dodano"
            self.ids.code_input.text = ""


class DeleteRegistrationScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        self.options = None
        self.exists = False
        self.registrations = None

    def on_enter(self):
        self.registrations = self.db.get_user_registrations(self.auth.user['localId'])
        self.options = self.ids.options
        layout = self.ids.options
        print(self.registrations)
        if self.registrations is not None:
            self.exists = True
            for registration in self.registrations:
                button = ToggleButton(text=registration)
                layout.add_widget(button)
        elif not self.exists:
            self.ids["success_label"].text = "Nie masz żadnych rejestracji"

    def delete_selected(self):

        if self.exists:
            selected_options = []
            for child in self.options.children:
                if isinstance(child, ToggleButton) and child.state == 'down':
                    selected_options.append(child.text)
                    if len(selected_options) == len(self.registrations):
                        self.exists = False
                    self.db.delete_registration_db(self.auth.user['localId'], child.text)
            print("Zaznaczone opcje:", selected_options)
            self.ids["success_label"].text = "Pomyślnie usunięto rejestracje"

            self.options.clear_widgets()
            for registration in self.registrations:
                button = ToggleButton(text=registration)
                if registration not in selected_options:
                    button.state = 'normal'
                self.options.add_widget(button)
            self.on_leave()
            self.on_enter()

    def refresh_page(self, dt):
        self.manager.current = 'settings'
        self.manager.current = 'deleteregistration'
    def on_leave(self, *args):
        layout = self.ids.options
        layout.clear_widgets()
        success_label = self.ids["success_label"]
        success_label.text = ""

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
    def __init__(self, auth, db,  **kw):
        super().__init__(**kw)
        self.auth = auth
        self.db = db
        self.receiver_id = None
        self.registration = None

    def on_enter(self, *args):
        self.receiver_id = self.manager.transition.args.get('receiver_id')
        self.registration = self.manager.transition.args.get('registration')
        if self.receiver_id:
            rounded_input = self.ids.registration
            rounded_input.text = self.registration

    def send_email(self, message, receiver_id):
        email = 'kokoskivy@gmail.com'
        password = 'gzuyzkittnadfhso'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        receiver_email = self.db.get_user_data(receiver_id).child('email').get().val()
        sender_username = self.db.get_user_data(self.auth.user['localId']).child('username').get().val()
        message = sender_username + " napisał: " + message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = receiver_email
        msg['Subject'] = "Wiadomość w aplikacji KOKOS"
        msg.attach(MIMEText(message))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, receiver_email, text)
            server.quit()
            print('Wiadomość została wysłana.')
        except Exception as e:
            print('Wystąpił błąd podczas wysyłania wiadomości: ', e)

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
        self.ids.result.text = ''
        if self.db.get_user_data(self.receiver_id).get().val()['email'] != '':
            self.send_email(message, self.receiver_id)


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
        screen_manager.add_widget(SettingsScreen(auth_service, data_provider, name='settings'))
        screen_manager.add_widget(AddDamageScreen(auth_service, data_provider, name='damage'))
        screen_manager.add_widget(YourQrCodeScreen(auth_service, data_provider, name='yourqrcode'))
        screen_manager.add_widget(AddRegistrationScreen(auth_service, data_provider, name='addregistration'))
        screen_manager.add_widget(DeleteRegistrationScreen(auth_service, data_provider, name='deleteregistration'))
        screen_manager.add_widget(UpdateUsernameScreen(auth_service, data_provider, name='updateusername'))


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
                self.root.current = 'main'
                return True
            elif self.root.current == 'addregistration':
                self.root.transition.direciton = "right"
                self.root.current = 'settings'
                return True
            elif self.root.current == 'deleteregistration':
                self.root.transition.direciton = "right"
                self.root.current = 'settings'
                return True
            elif self.root.current == 'updateusername':
                self.root.transition.direciton = "right"
                self.root.current = 'settings'
                return True
if __name__ == '__main__':
    MyApp().run()


