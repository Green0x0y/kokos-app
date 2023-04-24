from kivy.uix.screenmanager import ScreenManager, Screen
from data.AuthService import AuthService



class LoginScreen(Screen):

    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        # self.ref = db.reference('users')
        self.auth = auth_service

    def login(self, instance):
        email_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        success, text = self.auth.login(email=email_input, password=password_input)
        error_label = self.ids["error_label"]
        if success:
            self.manager.current = 'main'
        error_label.text = text


    def move_to_signup(self, instance):
        self.manager.current = 'signup'