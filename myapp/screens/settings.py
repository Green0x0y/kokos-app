from kivy.uix.screenmanager import Screen

class SettingsScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def switch_click(self, switchObject, switchValue):
        if (switchValue):
            self.ids.mail_label.text = "Powiadomienia mailowe on"
            self.db.email_notifications_on(self.auth.user['localId'])
        else:
            self.ids.mail_label.text = "Powiadomienia mailowe off"
            self.db.email_notifications_off(self.auth.user['localId'])

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