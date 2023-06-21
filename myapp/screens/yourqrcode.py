import base64
import qrcode
from data.DataProvider import DataProvider
from kivy.uix.screenmanager import Screen
from io import BytesIO


class YourQrCodeScreen(Screen):

    def __init__(self, auth_service, db: DataProvider, **kw):
        super().__init__(**kw)
        self.auth = auth_service
        self.db = db

    def on_enter(self, *args):
        qr_data = self.db.get_current_user_data()['qr_code']
        qr = qrcode.QRCode(version=1, box_size=20, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert PIL Image to RGBA and then to base64
        img_rgba = img.convert('RGBA')
        buffered = BytesIO()
        img_rgba.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Update the source of the Image widget to display the QR code
        self.ids.qr_code_image.source = f'data:image/png;base64,{img_str}'
        self.ids.qr_code_image.reload()
