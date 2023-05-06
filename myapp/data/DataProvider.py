import firebase
import data.AuthService as AuthService
import json
import asyncio

class DataProvider:
    def __init__(self, firebase: firebase, auth_service: AuthService) -> None:
        self.db = firebase.database()
        self.current_user_data = self.db.child("users").child("ktos").get().val()
        self.auth_service = auth_service
    def get_conversations(self):
        return self.db.child("conversations").child("conversation_to")
    def get_conversation_messages(self, user):
        return self.db.child("conversations").child("conversation_to").child(user)
    def get_user_data(self, uid):
        return self.db.child("users").child(uid)
    
    def get_current_user_data(self):
        return self.current_user_data   
    
    def set_current_user_data(self, uid):
        self.current_user_data = self.db.child("users").child(uid).get().val()

    def add_user_data(self, user_data, uid):
        self.current_user_data = user_data
        self.db.child("users").child(str(uid)).set(user_data)