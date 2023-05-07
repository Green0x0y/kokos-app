import firebase
import data.AuthService as AuthService
from datetime import datetime
import json
import asyncio

class DataProvider:
    def __init__(self, firebase: firebase, auth_service: AuthService) -> None:
        self.db = firebase.database()
        self.current_user_data = self.db.child("users").child("a").get().val()
        self.auth_service = auth_service

    def get_users(self):
        return self.db.child("users")

    def get_conversations(self, receiver):
        return self.db.child("users").child(receiver).child("conversations").child("conversation_to")

    def get_conversation_messages(self, receiver, sender):
        return self.db.child("users").child(receiver).child("conversations").child("conversation_to").child(sender)

    def add_message(self, message, sender, reciver):
        self.db.child("users").child(reciver).child("conversations").child("conversation_to").child(sender).push(
            {
            'datetime':   datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'message': message
            })

    def get_datetime(self, msg):
        return msg.child

    def get_user_data(self, uid):
        return self.db.child("users").child(uid)

    
    def get_current_user_data(self):
        return self.current_user_data
    
    def set_current_user_data(self, uid):
        self.current_user_data = self.db.child("users").child(uid).get().val()

    def add_user_data(self, user_data, uid):
        self.current_user_data = user_data
        self.db.child("users").child(str(uid)).set(user_data)