from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
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


class ChatsScreen(Screen):
    def __init__(self, auth_service, db, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db
        self.initiated = False
# to jest zdecydowanie do zrefactorowania, ale for now działa
    def on_enter(self, *args):

        def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size
        
        if self.initiated: return
        conversation_IDs = self.db.get_conversations_IDs(self.auth.get_uid())
        chatsPanel = TabbedPanel(do_default_tab=False, tab_pos='left_mid')

        with chatsPanel.canvas.before:
            Color(133/255, 106/255, 85/255, 1) # brown
            chatsPanel.rect = Rectangle(pos=chatsPanel.pos, size=chatsPanel.size)
        chatsPanel.bind(pos=update_rect, size=update_rect)

        if conversation_IDs is not None and len(conversation_IDs) != 0:
            first_tab = True
            for conv in conversation_IDs:
                chat = ChatWindow(self.db, self.auth, conv)
                chatsPanel.add_widget(chat)
                if first_tab:
                    chat.on_press()
                    chatsPanel.set_def_tab = chat
                    first_tab = False

        self.add_widget(chatsPanel)
        self.initiated = True


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
        # self.text_size = None,  self.width/5
        self.font_size = self.width/6
        self.color = 133/255, 106/255, 85/255, 1
        self.background_color = 223/255, 223/255, 213/255, 1
        self.background_normal = ''
        self.background_down = ''
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
        self.parent_xd = parent
        self.db = db 
        self.conversation = conv

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.add_widget(self.layout)
        with self.canvas.before:
            Color(0.913,0.893, 0.891, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.user_data_stream = self.db.get_conversation_for_stream(self.conversation).stream(self.stream_handler)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def stream_handler(self, message):
        if message['path'] == '/':
            for msg in message['data'].values():
                Clock.schedule_once(partial(self.add_msg_callback, msg), 0)
        else:
            Clock.schedule_once(partial(self.add_msg_callback, message['data']), 0)

    def add_msg_callback(self, msg, *largs):
        new_message = Message(self.parent_xd, msg['from'] + " on " + msg['datetime'] + " wrote: ", msg['message'], msg['to'])
        self.layout.add_widget(new_message)

class Message(BoxLayout):
    def __init__(self, parent, text, msg, receiver, **kwargs):
        super(Message, self).__init__(**kwargs)

        self.orientation='vertical'
        self.spacing = 5
        self.width = parent.width
        self.padding = [10, 10]
        self.size_hint_y = None
        print(receiver, parent.user)
        if receiver != parent.user:
            msg_label = MessageLabel(self, text, pos_hint={'right': 1})
            msg_box = StackLayout(orientation='rl-tb')
            msg_content = MessageContent(parent, msg, bg_color=(0, 1, 0, 1))
            msg_del = Button(text="del", width=20,size_hint=(0.2, 1))
            msg_box.add_widget(msg_content)
            msg_box.add_widget(msg_del)
        else:
            msg_label = MessageLabel(self, text, pos_hint={'left': 1})
            msg_box = MessageContent(parent, msg, bg_color=(1, 1, 1, 1), pos_hint={'left': 1})
        self.add_widget(msg_label)
        self.add_widget(msg_box)
        # if receiver != parent.user: self.add_widget(msg_del)

class MessageContent(Label):
    def __init__(self, parent, text, bg_color, **kwargs):
        super(MessageContent, self).__init__(**kwargs)
        self.text = text
        self.size_hint_x= None
        self.font_size = parent.parent.height/3
        self.font_name = 'Roboto-Bold.ttf'
        self.color = 0, 0, 0, 1
        self.bold=True
        self.padding = (30, 10)
        self.texture_update()
        # print(self.texture_size[0], Window.width, text)
        if self.texture_size[0] > Window.width:
            self.width = Window.width
            self.text_size = (Window.width*0.8, None)
        else:
            self.width = self.texture_size[0]

        self.halign = 'left'

        with self.canvas.before:
            Color(*bg_color)
            print("self.size:", self.size)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        print("size calling rect", self.size)
        self.rect.pos = self.pos
        self.texture_update()
        self.rect.size = self.texture_size
        # return self.texture_size
        print("size calling rect after texture update", self.size, self.texture_size)

class MessageLabel(Label):
    def __init__(self, parent, text, **kwargs):
        super(MessageLabel, self).__init__(**kwargs)
        self.text = text
        self.size_hint_x = None
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
            Color(0.913,0.893, 0.891, 1)
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
    
