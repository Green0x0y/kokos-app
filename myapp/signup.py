import firebase
from kivy.uix.screenmanager import Screen


class SignUpScreen(Screen):

    def __init__(self, auth_serive, data_provider, **kw):
        super().__init__(**kw)
        self.users = data_provider.users
        self.auth = auth_serive

    def check_passwords(self, password, password2):
        return password == password2

    def check_valid_email(self, email):
        return '@' in email
    
    def switch_to_login_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'login'

    def add_user(self, instance):
        username_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        email_input = self.ids.email_input.text
        password_input_2 = self.ids.password_input_2.text
        error_label = self.ids["error_label"]
        
        if not self.check_passwords(password_input, password_input_2):
            error_label.text = "Hasła nie są takie same"
        elif username_input == "" or email_input == "" or password_input == "" or password_input_2 =="":
            error_label.text = "Uzupełnij wszystkie pola"
        elif len(password_input) < 7:
            error_label.text = "Hasło musi mieć conajmniej 7 znaków"
        else:
            user_data = {
                'username': username_input,
                'qr_code': '',
                'registrations': {}
            }

            success, text, uid = self.auth.signup(email_input, password_input, username_input)
            error_label.text = text
            if success:
                self.users.child(uid).set(user_data)
                # user = self.auth.create_user(email=email_input, password=password_input)
                self.manager.current ='main';
