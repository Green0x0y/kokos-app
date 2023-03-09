from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Builder.load_file('loginscreen.kv')
Builder.load_file('mainscreen.kv')
Builder.load_file('usercodescreen.kv')
Builder.load_file('registrationscreen.kv')

class LoginScreen(Screen):
    def login(self, instance):

        # Check if the username and password are correct
        if self.ids.username_input.text == 'admin' and self.ids.password_input.text == 'admin123':
            # Switch to the main screen
            self.manager.current = 'main'
            self.ids.username_input.text = ''
            self.ids.password_input.text = ''





class MainScreen(Screen):


    def switch_to_user_code_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'user_code'
    def switch_to_registration_screen(self, instance):
        # Switch to the user code screen
        self.manager.current = 'registration'

class UserCodeScreen(Screen):
    def verify_code(self, instance):
        code = self.ids.code_input.text
        if len(code) != 8:
            print("Code must be 8 characters long")
        elif not code.isalnum():
            print("Code must contain only letters and numbers")
        else:
        # TODO: Handle valid code
            print("Valid code entered")

class RegistrationScreen(Screen):
    def verify_code(self, instance):
        code = self.ids.code_input.text
        if len(code) != 8:
            print("Code must be 8 characters long")

class MyApp(App):
    username =''
    def build(self):

        Window.bind(on_keyboard=self.on_key)
        # Create the screen manager and add the login and main screens to it
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(RegistrationScreen(name='registration'))

        screen_manager.add_widget(MainScreen(name='main'))

        screen_manager.add_widget(UserCodeScreen(name='user_code'))




        return screen_manager



    def on_key(self, window, key, *args):

        if key == 27:  # 27 is the keycode for the back button
            # Switch to the previous screen
            if self.root.current == 'user_code':
                self.root.current = 'main'
                return True
            elif self.root.current == 'registration':
                self.root.current = 'main'
                return True


if __name__ == '__main__':
    MyApp().run()


