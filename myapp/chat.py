from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.core.window import Window
from kivy.lang import Builder
from data.DataProvider import DataProvider
from data.AuthService import AuthService

Builder.load_file('custom_widgets/roundedinput.kv')
Builder.load_file('custom_widgets/roundedbutton.kv')


class ChatWindow(TabbedPanelItem):
    def __init__(self, db: DataProvider, auth: AuthService, conversation, **kwargs):
        super(ChatWindow, self).__init__(**kwargs)
        self.db = db
        self.auth = auth
        self.user = self.auth.get_uid()
        self.conversation = conversation
        self.receiver = self.db.get_other_uid(self.user, self.conversation)
        self.created = False
        self.username = self.db.get_username(self.receiver)
        self.text = self.username


    def send_message(self, instance):
        message = self.send_input.text
        self.db.add_message(message, self.auth.get_uid(), self.receiver)


    def on_press(self):
        # print(touch)
        if self.created:
            return
        user_data = self.db.get_conversation(self.conversation)
        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        chat_box = ChatBox(self, self.username, user_data, self.db, self.conversation)

        send_message = SendMessage()
        send_button = RoundedButton("send")
        send_button.bind(on_press=self.send_message)
        self.send_input = TextInput()
        self.send_input.id = "msg_to_send"

        send_message.add_widget(self.send_input)
        send_message.add_widget(send_button)

        layout.add_widget(chat_box)
        layout.add_widget(send_message)
        self.add_widget(layout)

        self.created = True



class ChatBox(ScrollView):
    def __init__(self, parent, user, user_messages, db, conv, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.size_hint=(1, 0.9)
        self.margin=10
        self.parent5 = parent
        self.db = db 
        self.conversation = conv

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        for msg in user_messages:
            msg_val = msg.val()
            print(msg_val, user)
            sender = parent.db.get_username(msg_val['from'])
            new_message = Message(parent, sender + " on " + msg_val['datetime'] + " wrote: ", msg_val['message'])
            self.layout.add_widget(new_message)

        self.add_widget(self.layout)
        with self.canvas.before:
            Color(0.4, 0.6, 1, 1) # blue color
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.user_data_stream = self.db.get_conversation_for_stream(self.conversation).stream(self.stream_handler)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def stream_handler(self, msg):
        print("msg:", msg['data'])
        # msg_val = msg['data'][self.bar_margin]
        # user = msg['data'].key()
        # print(msg_val, user)
        # new_message = Message(self.parent, user + " on " + msg_val['datetime'] + " wrote: ", msg_val['message'])
        # self.layout.add_widget(new_message)
        # print(message["event"]) # put
        # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
        # print(message["data"]) # {'title': 'Firebase', "body": "etc..."}

class Message(BoxLayout):
    def __init__(self, parent, text, msg, **kwargs):
        super(Message, self).__init__(**kwargs)

        self.orientation='vertical'
        self.spacing = 5
        self.padding = [10, 10]
        self.size_hint_y = None
        self.add_widget(MessageLabel(text))
        label = MessageContent(parent, msg)

        self.add_widget(label)

class MessageContent(Label):
    def __init__(self, parent, text, **kwargs):
        super(MessageContent, self).__init__(**kwargs)
        self.text = text
        self.size_hint_x= None
        self.color = 0, 0, 0, 1
        self.font_size = parent.parent.height/5
        self.font_name = 'Roboto-Bold.ttf'
        self.bold=True
        self.padding = (30, 100)
        self.texture_update()
        self.width = self.texture_size[0]

        with self.canvas.before:
            Color(1, 1, 1, 1) # white
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MessageLabel(Label):
    def __init__(self, text, **kwargs):
        super(MessageLabel, self).__init__(**kwargs)
        self.text = text
        self.size_hint_x= None
        self.color = 0.2, 0.2, 0.2, 0.7
        self.font_name = 'Roboto-Bold.ttf'
        self.texture_update()
        self.width = self.texture_size[0]

class SendMessage(BoxLayout):
    def __init__(self, **kwargs):
        super(SendMessage, self).__init__(**kwargs)

        self.orientation='horizontal'
        self.size_hint=(1, 0.1)
        self.spacing= 30
        self.padding = 10

        with self.canvas.before:
            Color(0.4, 0.6, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)


    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class RoundedButton(Button):
    def __init__(self, text, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

        self.size_hint = (0.2, 1)
        self.text = text

class RoundedInput(TextInput):
    def __init__(self, **kwargs):
        super(TextInput, self).__init__(**kwargs)
    
