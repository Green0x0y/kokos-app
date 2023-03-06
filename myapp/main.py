from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('loginscreen.kv')
Builder.load_file('mainscreen.kv')


class LoginScreen(Screen):
    def login(self, instance):

        # Check if the username and password are correct
        if self.ids.username_input.text == 'admin' and self.ids.password_input.text == 'admin123':
            # Switch to the main screen
            self.manager.current = 'main'
            self.ids.username_input.text = ''
            self.ids.password_input.text = ''



class MainScreen(Screen):
    def logout(self, instance):
    # Switch back to the login screen
        self.manager.current = 'login'

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


class MyApp(App):
    username =''
    def build(self):
        # Create the screen manager and add the login and main screens to it
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(UserCodeScreen(name='user_code'))

        return screen_manager


if __name__ == '__main__':
    MyApp().run()


