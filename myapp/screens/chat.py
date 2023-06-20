from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from data.DataProvider import DataProvider
from data.AuthService import AuthService
from kivy.clock import Clock
from functools import partial
from kivy.modules import inspector

Builder.load_file('GUI/custom_widgets/roundedinput.kv')
Builder.load_file('GUI/custom_widgets/roundedbutton.kv')
Builder.load_file('GUI/chat_utils/chatwindow.kv')
Builder.load_file('GUI/chat_utils/othermessage.kv')
Builder.load_file('GUI/chat_utils/mymessage.kv')
Builder.load_file('GUI/chat_utils/chatbox.kv')
Builder.load_file('GUI/chat_utils/sendarea.kv')
Builder.load_file('GUI/chat_utils/message.kv')


class ChatScreen(Screen):
    def __init__(self, auth_service: AuthService, db: DataProvider, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        self.chatsPanel = self.ids.chats_panel
        self.initiated = False
        self.first_tab = None

    def on_enter(self, *args):
        if self.initiated: return
        self.init_chats()
        self.initiated = True

    def init_chats(self):
        self.db.get_conversations_IDs_for_stream(self.auth.get_uid()).stream(self.new_chat_handler)
        
    def new_chat_handler(self, covnersation_IDs):
        data = covnersation_IDs['data']
        data = {} if data is None else data 
        for conv_id in data:
            if data[conv_id]:
                Clock.schedule_once(partial(self.add_chat_callback, conv_id))

    def add_chat_callback(self, conv_id, *args):
        new_chat = ChatWindow(self.db, self.auth, conv_id)
        self.chatsPanel.add_widget(new_chat)


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
        self.bind(state=self.update_active_tab)
        inspector.create_inspector(Window, self)
    
    def send_message(self, instance):
        message = self.send_input.text
        if message != "":
            self.db.add_message(message, self.auth.get_uid(), self.receiver, self.db.current_user_data['username'])
        self.send_input.text = ""

    def update_active_tab(self, header, state):
        if state == 'down':
            header.background_color = 106/255, 231/255, 75/255, 1
        else:
            header.background_color = 223/255, 223/255, 213/255, 1

    def on_press(self):
        if self.created:
            return
        self.init_tab()
        self.created = True
    
    def init_tab(self):
        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        chat_box = ChatBox(self, self.db, self.conversation)
        send_area = SendArea()

        self.send_input = send_area.ids.input

        send_button = send_area.ids.send
        send_button.bind(on_press=self.send_message)

        layout.add_widget(chat_box)
        layout.add_widget(send_area)
        self.add_widget(layout)


class ChatBox(ScrollView):
    def __init__(self, parent, db, conv: str, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.user_id = parent.user
        self.db = db 
        self.conv = conv
        self.messages = {}

        self.layout = self.ids.messages
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.db.get_conversation_for_stream(self.conv).stream(self.conversation_handler)

    def conversation_handler(self, message):
        # print(message)
        messages = {} if message['data'] is None else message['data']
        if message['path'] == '/':
            for msg_id, msg in messages.items():
                Clock.schedule_once(partial(self.add_msg_callback, msg, msg_id), 0)
        elif messages: # special case, when there is only one message
            msg_id = message['path'].replace("/", "")
            Clock.schedule_once(partial(self.add_msg_callback, message['data'], msg_id), 0)
        else: # case when the message is deleted
            msg_id = message['path'].replace("/", "")
            Clock.schedule_once(partial(self.remove_msg_callback, self.messages[msg_id]), 0)
            
    def remove_msg_callback(self, msg, *args):
        self.layout.remove_widget(msg)

    def add_msg_callback(self, msg, msg_id, *args):
        label =  msg['datetime']+ ": " + msg['from'] + " napisał/a: "
        if(msg['to'] != self.user_id):
            new_message = MyMessage( label, msg['message'], self.db, msg_id, self.conv)
        else:
            new_message = OtherMessage(label, msg['message'])
        self.messages[msg_id] = new_message
        self.layout.add_widget(new_message)

class SendArea(BoxLayout):
    def __init__(self, **kwargs):
        super(SendArea, self).__init__(**kwargs)

class MyMessage(BoxLayout):
    def __init__(self, text, msg, db: DataProvider, msg_id, conv_id, **kwargs):
        super(MyMessage, self).__init__(**kwargs)
        self.db = db
        self.msg_id = msg_id
        self.conv_id = conv_id
        self.ids.label.text = text
        self.ids.content.text = msg
        self.ids.delete.bind(on_release=self.del_message)

    def del_message(self, instance):
        self.db.delete_message(self.msg_id, self.conv_id)
 
class OtherMessage(BoxLayout):
    def __init__(self, text, msg, **kwargs):
        super(OtherMessage, self).__init__(**kwargs)
        self.ids.label.text = text
        self.ids.content.text = msg
    
