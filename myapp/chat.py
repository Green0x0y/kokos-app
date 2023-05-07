from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('custom_widgets/roundedinput.kv')
Builder.load_file('custom_widgets/roundedbutton.kv')

class ChatWindow(TabbedPanelItem):
    def __init__(self, db, auth,  receiver, user_data, **kwargs):
        super(ChatWindow, self).__init__(**kwargs)
        self.text=receiver
        self.db = db
        self.auth = auth
        self.receiver = receiver

        self.username = self.db.get_user_data(receiver).get().val()['username']

        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        chat_box = ChatBox(self, self.username, user_data)


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

    def send_message(self, instance):
        message = self.send_input.text
        self.db.add_message(message, self.auth.get_uid(), self.receiver)


class ChatBox(ScrollView):
    def __init__(self, parent, user, user_messages, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.size_hint=(1, 0.9)
        self.margin=10

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for msg in user_messages:
            msg_val = msg.val()
            new_message = Message(parent, user + " on " + msg_val["datetime"] + " wrote: ", msg_val["message"])
            layout.add_widget(new_message)

        self.add_widget(layout)
        with self.canvas.before:
            Color(0.4, 0.6, 1, 1) # blue color
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

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
        self.font_size = parent.height/5
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
    
