import firebase
import data.AuthService as AuthService
import json
import asyncio

class DataProvider:
    def __init__(self, firebase: firebase, auth_service: AuthService) -> None:
        self.db = firebase.database()
        self.users = self.db.child("users")
        self.current_user_data = self.users.child("ktos").get().val()
        self.auth_service = auth_service

    def get_user_data(self, uid):
        return self.users.child(uid)
    
    def get_current_user_data(self):
        return self.current_user_data   
    
    def set_current_user_data(self, uid):
        self.current_user_data = self.users.child(uid).get().val()

    def add_user_data(self, user_data, uid):
        self.current_user_data = user_data
        self.db.child("users").child(str(uid)).set(user_data)
          