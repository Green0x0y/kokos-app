from kivy.uix.screenmanager import Screen


class RegistrationScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def find_user_by_registration(self, registration):
        users = self.db.get_users().get()
        for user in users.each():
            user_data = self.db.get_user_data(user.key()).child('registrations').get().val()
            print(user_data)
            if user_data is not None and registration in user_data:
                return user.key(), ""
        else:
            return None, ""

    def go_to_chat(self, instance):
        registration = self.ids.code_input.text
        error_label = self.ids["error_label"]
        error_label.text = ""
        if len(registration) != 7:
            error_label.text = "Nieprawidłowa dłogość"
        userId, error = self.find_user_by_registration(registration)
        error_label.text = error

        if not userId:
            error_label.text = "Nie ma takiej rejestracji"
        else:
            self.manager.transition.args = {'receiver_id': userId, 'registration': registration}
            self.manager.current = 'damage'
            error_label.text = ""
