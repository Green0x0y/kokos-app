from kivy.uix.screenmanager import Screen


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