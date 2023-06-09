from kivy.uix.screenmanager import Screen
from requests.exceptions import HTTPError
from data.AuthService import AuthService


class ForgotPasswordScreen(Screen):
    def __init__(self, auth_service: AuthService, **kw):
        self.auth = auth_service
        super().__init__(**kw)

    def send_passwd_reset(self, instance):
        email = self.ids.reset_email_input.text
        try:
            self.auth.reset_password(email)
            self.manager.current = 'login'
        except HTTPError as e:
            self.ids.error_label.text = "invalid email"