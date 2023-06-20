import firebase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from data.AuthService import AuthService
from data.DataProvider import DataProvider
from kivy_garden.zbarcam import ZBarCam
# import json

from screens.adddamage import AddDamageScreen
from screens.addregistration import AddRegistrationScreen
from screens.chat import ChatScreen
from screens.deleteregistration import DeleteRegistrationScreen
from screens.forgotpassword import ForgotPasswordScreen
from screens.login import LoginScreen
from screens.main import MainScreen
from screens.qr import QRScreen
from screens.registration import RegistrationScreen
from screens.settings import SettingsScreen
from screens.signup import SignUpScreen
from screens.updateusername import UpdateUsernameScreen
from screens.usercode import UserCodeScreen
from screens.yourqrcode import YourQrCodeScreen

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
Builder.load_file('screens/addregistrationscreen.kv')
Builder.load_file('screens/deleteregistrationscreen.kv')
Builder.load_file('screens/updateusernamescreen.kv')
Builder.load_file('screens/forgotpasswordscreen.kv')
Builder.load_file('screens/chatscreen.kv')
Window.size = (500, 700)


class MyApp(App):
    def build(self):
        screens = [LoginScreen(auth_service, data_provider, name='login'),
                   MainScreen(auth_service, data_provider, name='main'),
                   QRScreen(auth_service, data_provider, name='qr'),
                   RegistrationScreen(auth_service, data_provider, name='registration'),
                   UserCodeScreen(name='user_code'),
                   SignUpScreen(auth_service, data_provider, name='signup'),
                   ChatScreen(auth_service, data_provider, name='chats'),
                   SettingsScreen(auth_service, data_provider, name='settings'),
                   AddDamageScreen(auth_service, data_provider, name='damage'),
                   YourQrCodeScreen(auth_service, data_provider, name='yourqrcode'),
                   AddRegistrationScreen(auth_service, data_provider, name='addregistration'),
                   DeleteRegistrationScreen(auth_service, data_provider, name='deleteregistration'),
                   UpdateUsernameScreen(auth_service, data_provider, name='updateusername'),
                   ForgotPasswordScreen(auth_service, name='forgot_password')]

        screen_manager = ScreenManager()
        for screen in screens:
            screen_manager.add_widget(screen)
        
        Window.bind(on_keyboard=self.on_key)
        
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
