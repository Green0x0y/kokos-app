from kivy.uix.screenmanager import Screen


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
            if user_registrations is not None and new_registration in user_registrations:
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
