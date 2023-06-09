from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton

class DeleteRegistrationScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        self.options = None
        self.exists = False
        self.registrations = None

    def on_enter(self):
        self.registrations = self.db.get_user_registrations(self.auth.user['localId'])
        self.options = self.ids.options
        layout = self.ids.options
        print(self.registrations)
        if self.registrations is not None:
            self.exists = True
            for registration in self.registrations:
                button = ToggleButton(text=registration)
                layout.add_widget(button)
        elif not self.exists:
            self.ids["success_label"].text = "Nie masz żadnych rejestracji"

    def delete_selected(self):

        if self.exists:
            selected_options = []
            for child in self.options.children:
                if isinstance(child, ToggleButton) and child.state == 'down':
                    selected_options.append(child.text)
                    if len(selected_options) == len(self.registrations):
                        self.exists = False
                    self.db.delete_registration_db(self.auth.user['localId'], child.text)
            print("Zaznaczone opcje:", selected_options)
            self.ids["success_label"].text = "Pomyślnie usunięto rejestracje"

            self.options.clear_widgets()
            for registration in self.registrations:
                button = ToggleButton(text=registration)
                if registration not in selected_options:
                    button.state = 'normal'
                self.options.add_widget(button)
            self.on_leave()
            self.on_enter()

    def refresh_page(self, dt):
        self.manager.current = 'settings'
        self.manager.current = 'deleteregistration'
    def on_leave(self, *args):
        layout = self.ids.options
        layout.clear_widgets()
        success_label = self.ids["success_label"]
        success_label.text = ""