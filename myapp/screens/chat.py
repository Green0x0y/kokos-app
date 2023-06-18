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



class ChatScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        self.initiated = False

    def on_enter(self, *args):
        if self.initiated: return
        self.init_chats()
        self.initiated = True

    def init_chats(self):
        IDs = self.db.get_conversations_IDs(self.auth.get_uid())
        chatsPanel = self.ids.chats_panel
        if IDs is not None and len(IDs) != 0:
            first_tab = True
            for conv_id in IDs:
                chat = ChatWindow(self.db, self.auth, conv_id)
                chatsPanel.add_widget(chat)
                if first_tab:
                    chat.on_press()
                    chatsPanel.set_def_tab = chat
                    first_tab = False


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

        send_button = send_area.ids.send
        send_button.bind(on_press=self.send_message)

        layout.add_widget(chat_box)
        layout.add_widget(send_area)
        self.add_widget(layout)


class ChatBox(ScrollView):
    def __init__(self, parent, db, conv, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.parent_xd = parent
        self.db = db 
        self.conversation = conv

        self.layout = self.ids.messages
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.db.get_conversation_for_stream(self.conversation).stream(self.stream_handler)

    def stream_handler(self, message):
        if message['path'] == '/':
            for msg in message['data'].values():
                Clock.schedule_once(partial(self.add_msg_callback, msg), 0)
        else:
            Clock.schedule_once(partial(self.add_msg_callback, message['data']), 0)

    def add_msg_callback(self, msg, *args):
        label = msg['from'] + " on " + msg['datetime'] + " wrote: "
        if(msg['to'] != self.parent_xd.user):
            new_message = MyMessage(self.parent_xd, label, msg['message'], msg['to'])
        else:
            new_message = OtherMessage(self.parent_xd, label, msg['message'], msg['to'])
        self.layout.add_widget(new_message)

class SendArea(BoxLayout):
    def __init__(self, **kwargs):
        super(SendArea, self).__init__(**kwargs)

class MyMessage(BoxLayout):
    def __init__(self, parent, text, msg, receiver, **kwargs):
        super(MyMessage, self).__init__(**kwargs)
        print(receiver, parent.user)
        self.ids.label.text = text
        self.ids.content.text = msg
 
class OtherMessage(BoxLayout):
    def __init__(self, parent, text, msg, receiver, **kwargs):
        super(OtherMessage, self).__init__(**kwargs)
        print(receiver, parent.user)
        self.ids.label.text = text
        self.ids.content.text = msg
    
