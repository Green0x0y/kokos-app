from kivy.uix.screenmanager import Screen

from kivy_garden.zbarcam import ZBarCam


class QRScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        
    def find_user_by_qr(self, qr_data):
        users = self.db.get_users().get()
        for user in users.each():
            user_qr_code = self.db.get_user_data(user.key()).child('qr_code').get().val()

            if user_qr_code is not None and qr_data == user_qr_code:
                print("kod" ,user_qr_code)
                return user.key(), ""
        else:
            return None, ""


    def switch_to_damage(self, instance, *args):
        symbol = instance.symbols[-1]  # Ostatni zeskanowany symbol
        qr_data = symbol.data.decode('utf-8')
        print(qr_data)
        userId, error = self.find_user_by_qr(qr_data)
        self.ids.qr_code_label.text = error

        if not userId:
            self.ids.qr_code_label.text = "Nie ma takiego kodu"
        else:
            self.manager.transition.args = {'receiver_id': userId, 'registration': 'Wczytano QR'}
            self.manager.current = 'damage'
            self.ids.qr_code_label.text  = ""
