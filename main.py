import asyncio
import threading
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO, Permission.INTERNET])

import cv2
import websockets

SERVER_URL = "ws://your-server-ip:8765"   # പിന്നീട് മാറ്റേണ്ടത്

class SecureCallApp(App):
    def build(self):
        self.title = "SecureCall"
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.status = Label(text="Welcome to SecureCall", size_hint_y=0.12, font_size=18)
        self.layout.add_widget(self.status)

        self.video_display = Image(size_hint_y=0.6, keep_ratio=True, allow_stretch=True)
        self.layout.add_widget(self.video_display)

        self.room_input = TextInput(
            hint_text="Enter Room ID (Example: room123)",
            multiline=False,
            size_hint_y=0.1,
            font_size=16
        )
        self.layout.add_widget(self.room_input)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.13, spacing=20)

        self.call_btn = Button(text="Start / Join Call", background_color=(0.1, 0.7, 0.3, 1), font_size=16)
        self.call_btn.bind(on_press=self.start_call)
        
        self.end_btn = Button(text="End Call", background_color=(0.8, 0.2, 0.2, 1), font_size=16)
        self.end_btn.bind(on_press=self.end_call)
        self.end_btn.disabled = True

        btn_layout.add_widget(self.call_btn)
        btn_layout.add_widget(self.end_btn)
        self.layout.add_widget(btn_layout)

        self.capture = None
        self.is_calling = False
        self.websocket = None
        self.room_id = ""

        return self.layout

    def start_call(self, instance):
        self.room_id = self.room_input.text.strip()
        if not self.room_id:
            self.status.text = "⚠️ Please enter Room ID!"
            return

        self.is_calling = True
        self.call_btn.disabled = True
        self.end_btn.disabled = False
        self.status.text = f"🔄 Connecting to Room: {self.room_id}..."

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_video, 1/25.0)

        threading.Thread(target=self.run_async, daemon=True).start()

    def run_async(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_websocket())

    async def connect_websocket(self):
        try:
            async with websockets.connect(SERVER_URL) as ws:
                self.websocket = ws
                await ws.send(json.dumps({"type": "join", "room": self.room_id}))
                self.status.text = f"🟢 Connected - Room: {self.room_id}"

                while self.is_calling:
                    await asyncio.sleep(0.1)
        except:
            self.status.text = "❌ Server Connection Failed"

    def update_video(self, dt):
        if self.capture and self.is_calling:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 0)
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.video_display.texture = texture

    def end_call(self, instance):
        self.is_calling = False
        self.call_btn.disabled = False
        self.end_btn.disabled = True
        self.status.text = "🔴 Call Ended"

        if self.capture:
            self.capture.release()
            self.capture = None

    def on_stop(self):
        self.end_call(None)

if __name__ == '__main__':
    SecureCallApp().run()