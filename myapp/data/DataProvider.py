import firebase
import data.AuthService as AuthService
from datetime import datetime
import json
import asyncio

class DataProvider:
    def __init__(self, firebase: firebase, auth_service: AuthService) -> None:
        self.db = firebase.database()
        self.current_user_data = None
        self.auth_service = auth_service

    def get_users(self):
        return self.db.child("users")

    def get_user_data(self, uid):
        return self.db.child("users").child(uid)
    
    def get_username(self, uid):
        return self.db.child("users").child(uid).get().val()['username']


    def get_current_user_data(self):
        return self.current_user_data
    
    def set_current_user_data(self, uid):
        self.current_user_data = self.db.child("users").child(uid).get().val()

    def add_user_data(self, user_data, uid):
        self.current_user_data = user_data
        self.db.child("users").child(str(uid)).set(user_data)

    def update_username(self, uid, new_username):
        self.db.child("users").child(uid).update({"username" : new_username})

    def get_user_registrations(self, uid):
        return self.db.child("users").child(uid).child("registrations").get().val()

    def add_registration_db(self, uid,  new_registration):
        registrations_array = self.db.child("users").child(uid).child("registrations").get().val()
        if registrations_array is not None:
            registrations_array = self.db.child("users").child(uid).child("registrations").get().val().copy()
        else:
            registrations_array = []
        registrations_array.append(new_registration)
        self.db.child("users").child(uid).update({"registrations": registrations_array})

    def delete_registration_db(self, uid, registration_to_delete):
        registrations_array = self.db.child("users").child(uid).child("registrations").get().val()
        if registrations_array is not None:
            registrations_array = self.db.child("users").child(uid).child("registrations").get().val().copy()
            registrations_array.remove(registration_to_delete)
            self.db.child("users").child(uid).update({"registrations": registrations_array})

    def add_conversation(self, message, sender, receiver):
        conversationID = self.get_conversationID(sender, receiver)
        conversations = self.db.child("users").child(sender).child("conversations").get().val()
        if conversations is None:
            conversations = {}
        conversations.update({conversationID: True})

        self.db.child("users").child(sender).child("conversations").update(conversations)
        if(sender != receiver):
            conversations = self.db.child("users").child(receiver).child("conversations").get().val()
            if conversations is None:
                conversations = {}
            conversations.update({conversationID: True})
            self.db.child("users").child(receiver).child("conversations").update(conversations)

        self.db.child("conversations").child(conversationID).push({
            'from' : sender,
            'to' : receiver,
            'datetime':   datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'message': message
        })
    def get_conversations_IDs(self, user: str) -> dict:
        return self.db.child("users").child(user).child("conversations").get().val()

    def get_conversation(self, ID: str) -> dict:
        return self.db.child("conversations").child(ID).get()
    
    def get_conversation_for_stream(self, ID: str):
        return self.db.child("conversations").child(ID)
    
    def add_message(self, message, sender, receiver, sender_nick):
        conversationID = self.get_conversationID(sender, receiver)
        self.db.child("conversations").child(conversationID).push({
            'from' : sender_nick,
            'to' : receiver,
            'datetime':   datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'message': message
        })

    def delete_message(self, msg_id, conversation):
        print("deleting msg", msg_id, conversation)

    def get_conversationID(self, sender, receiver):
        if sender > receiver:
            return sender + ":" + receiver
        else:
            return receiver + ":" + sender
    
    def get_other_uid(self, uid, conv_ID):
        other_id = conv_ID.replace(uid, "").replace(":", "")
        if other_id == "":
            other_id = uid
        return other_id