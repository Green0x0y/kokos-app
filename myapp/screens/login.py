from kivy.uix.screenmanager import ScreenManager, Screen
from data.AuthService import AuthService
from data.DataProvider import DataProvider
from kivy.modules import inspector
from kivy.core.window import Window



class LoginScreen(Screen):

    def __init__(self, auth_service: AuthService, db: DataProvider, **kw):
        super().__init__(**kw)
        self.db = db
        self.auth = auth_service
        inspector.create_inspector(Window, self)

    def login(self, instance):
        email_input = self.ids.username_input.text
        password_input = self.ids.password_input.text
        success, text = self.auth.login(email=email_input, password=password_input)
        error_label = self.ids["error_label"]
        if success:
            self.db.set_current_user_data(self.auth.get_uid())
            self.manager.current = 'main'
        error_label.text = text

    def move_to_signup(self, instance):
        self.manager.current = 'signup'

    def move_to_forgot_password(self, instance):
        self.manager.current = 'forgot_password'