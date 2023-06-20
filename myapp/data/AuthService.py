import requests
import json
import firebase
import hashlib
import string
import re


class AuthService:
    def __init__(self, firebase: firebase) -> None:
        self.auth = firebase.auth()
        self.user = {
            'localId': "GBt7wQuHPDUwU7z4AeW8Dxac7np2"
        }

    def login(self, email: str, password: str):
        email = "sebastian@gmail.com"
        password = "Password!1"
        # does not check for permission denied error
        # email = "b@b.com"
        # password = "Password1!"
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
            print('Successfully signed in user:', self.user['localId'])
            return True, ""
        except requests.HTTPError as e:
            err = json.loads(e.args[1])['error']['message']
            print(err)
            return False, str(err)
    
    def signup(self, email: str, password: str, password_check: str):
        if not password == password_check:
            return False, "Hasła nie są takie same", None
        password_ok, error_password = self.check_password(password)
        email_ok, error_email = self.check_email(email)
        if password_ok and email_ok:
            try:
                user = self.auth.create_user_with_email_and_password(email, password)
                self.login(email, password)
                return True, "", user['localId']
            except requests.HTTPError as e:
                err = json.loads(e.args[1])['error']['message']
                return False, str(err), None
        elif email_ok:
            return False, error_password, None
        else:
            return False, error_email, None

    def get_uid(self) -> str:
        return str(self.user['localId'])

    def get_user(self):
        return self.user
    
    def check_password(self, password: str):
        if len(password) < 8:
            return False, "Hasło powinno zawierać conajmniej 8 znaków"
        digits, upper, lower, special = 0, 0, 0, 0
        for char in password:
            if (char.islower()):
                lower += 1
            if(char.isupper()):
                upper += 1
            if(char.isdigit()):
                digits += 1
            if(char in string.punctuation):
                special += 1

        if ( digits == 0):
            return False, "Hasło powinno zawierać conajmniej jedną cyfrę"
        elif ( upper == 0):
            return False, "Hasło powinno zawierać conajmniej jedną wielką literę"
        elif ( lower == 0):
            return False, "Hasło powinno zawierać conajmniej jedną małą literę"
        elif ( special == 0):
            return False, "Hasło powinno zawierać conajmniej jeden znak specjalny"
        elif ( digits + upper + lower + special != len(password)):
            return False, "Hasło zawiera nielegalne znaki, używaj tylko alfabetu łacińskiego, cyfr, i znaków specjalnych: !\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
        else:
            return True, ""
        
    def check_email(self, email: str):
        # email_regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        email_regex = "[^@]+@[^@]+\.[^@]+"
        if re.match(email_regex, email):
            return True, ""
        else:
            return False, "Niepoprawny adres email"
        
    def reset_password(self, email: str):
        self.auth.send_password_reset_email(email)

