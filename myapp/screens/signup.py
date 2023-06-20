import firebase
from kivy.uix.screenmanager import Screen
import hashlib
from collections import OrderedDict

class SignUpScreen(Screen):

    def __init__(self, auth_service, data_provider, **kw):
        super().__init__(**kw)
        self.db = data_provider
        self.auth = auth_service
    
    def switch_to_login_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'login'

    def add_user(self, instance):
        username_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        email_input = self.ids.email_input.text
        password_input_2 = self.ids.password_input_2.text
        error_label = self.ids["error_label"]
        
        if username_input == "" or email_input == "" or password_input == "" or password_input_2 =="":
            error_label.text = "Uzupełnij wszystkie pola"
        else:
            success, text, uid = self.auth.signup(email_input, password_input, password_input_2)

            error_label.text = text
            if success:
                email_hash = hashlib.sha256(email_input.encode()).hexdigest()
                user_data = OrderedDict({
                    'conversation': {
                        'conversation_to': {

                        }
                    },
                    'username': username_input,
                    'qr_code': email_hash,
                    'registrations': {},
                    'email': email_input,
                    'email_notifications': False,

                })
                self.db.add_user_data(user_data, uid)
                self.manager.current ='main';
