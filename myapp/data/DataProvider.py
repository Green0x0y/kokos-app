import firebase

class DataProvider:
    def __init__(self, firebase) -> None:
        self.db = firebase.database()
        self.users = self.db.child("users")
        self.user = None

    def get_user_data(self, uid):
        return self.users.child(uid)
    
    def add_user_data(self, user_data, user):
        return self.users.push(user_data, user['idToken'])
    

    