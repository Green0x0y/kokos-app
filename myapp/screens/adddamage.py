import smtplib
from kivy.uix.screenmanager import Screen
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AddDamageScreen(Screen):
    def __init__(self, auth, db,  **kw):
        super().__init__(**kw)
        self.auth = auth
        self.db = db
        self.receiver_id = None
        self.registration = None

    def on_enter(self, *args):
        self.receiver_id = self.manager.transition.args.get('receiver_id')
        self.registration = self.manager.transition.args.get('registration')
        if self.receiver_id:
            rounded_input = self.ids.registration
            rounded_input.text = self.registration

    def send_email(self, message, receiver_id):
        email = 'kokoskivy@gmail.com'
        password = 'gzuyzkittnadfhso'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        receiver_email = self.db.get_user_data(receiver_id).child('email').get().val()
        sender_username = self.db.get_user_data(self.auth.user['localId']).child('username').get().val()
        message = sender_username + " napisał: " + message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = receiver_email
        msg['Subject'] = "Wiadomość w aplikacji KOKOS"
        msg.attach(MIMEText(message))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, receiver_email, text)
            server.quit()
            print('Wiadomość została wysłana.')
        except Exception as e:
            print('Wystąpił błąd podczas wysyłania wiadomości: ', e)

    def send(self):
        message = self.ids.message.text
        if message == "":
            return
        # self.manager.transition.args = {'message': message}
        # self.db.add_message(message, auth_service.user['localId'], self.receiver_id)\
        self.db.add_conversation(message, self.auth.user['localId'], self.receiver_id)
        self.ids.message.text = ''
        self.ids.result.text = 'Wiadomość wysłana!'
        self.manager.transition.args = {"to": self.receiver_id}
        self.manager.current = 'chats'
        self.ids.result.text = ''
        if self.db.get_user_data(self.receiver_id).get().val()['email'] != '' \
                and self.db.get_email_notifications_setting(self.receiver_id):
            self.send_email(message, self.receiver_id)
