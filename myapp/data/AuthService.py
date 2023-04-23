import firebase
import requests
import json

class AuthService:
    def __init__(self, firebase) -> None:
        self.auth = firebase.auth()
        self.user = None      

    def login(self, email: str, password: str):
        # does not check for permission denied error
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
            print('Successfully signed in user:', self.user)
            return True, ""
        except requests.HTTPError as e:
            err = json.loads(e.args[1])['error']['message']
            print(err)
            return False, str(err)
    
    def signup(self, email: str, password: str, username):
        success, text = self.check_user_exists(email, username)
        if not success:
            try:
                user = self.auth.create_user_with_email_and_password(email, password)
                self.login(email, password)
                return True, "", user['localId']
            except requests.HTTPError as e:
                err = json.loads(e.args[1])['error']['message']
                return False, str(err)
        else:
            return False, text

    def get_user(self):
        return self.user
    
    def check_user_exists(self,email, username):
        return False, ""

        # users = self.ref.get()

        # if users is not None:
        #     for user_id, user in users.items():
        #         if user.get('email') == email:
        #             return True, "Email już istnieje"
        #         if user_id == username:
        #             return True, "Nazwa użytkownika zajęta"

