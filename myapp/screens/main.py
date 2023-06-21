from kivy.uix.screenmanager import Screen
from data.DataProvider import DataProvider
from data.AuthService import AuthService


class MainScreen(Screen):
    # user_data = self.db.get_user_data(auth_service.user['localId']).get()
    def __init__(self, auth: AuthService, data_provider: DataProvider, **kw):
        super().__init__(**kw)
        self.auth = auth
        self.db = data_provider

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
        if self.auth.user is None:
            label.text = " unresgistered"
        label.text = "Cześć " + self.db.get_current_user_data()['username'] + "!"
