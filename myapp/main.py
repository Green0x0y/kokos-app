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


class MyApp(App):
    def build(self):
        # Create the screen manager and add the login and main screens to it
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(MainScreen(name='main'))

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
