"""
profile.py
-----------
شاشة الملف الشخصي: عرض بيانات المستخدم، تعديل الاسم/الهاتف، وتسجيل الخروج.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.metrics import dp

import database
from translation import tr
import screens.login as login


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))

        self.avatar = AsyncImage(source="assets/avatar_placeholder.png",
                                  size_hint=(1, 0.25))

        self.name_input = TextInput(hint_text=tr("full_name"), multiline=False,
                                     size_hint=(1, 0.09))
        self.phone_input = TextInput(hint_text=tr("phone"), multiline=False,
                                      size_hint=(1, 0.09))
        self.email_label = Label(text="", size_hint=(1, 0.08))

        save_btn = Button(text=tr("save"), size_hint=(1, 0.1),
                           background_color=(0.13, 0.13, 0.15, 1))
        save_btn.bind(on_release=self.save_profile)

        settings_btn = Button(text=tr("settings"), size_hint=(1, 0.1))
        settings_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "settings"))

        logout_btn = Button(text=tr("logout"), size_hint=(1, 0.1),
                             background_color=(0.6, 0.1, 0.1, 1))
        logout_btn.bind(on_release=self.logout)

        for w in (self.avatar, self.name_input, self.phone_input,
                  self.email_label, save_btn, settings_btn, logout_btn):
            root.add_widget(w)

        self.add_widget(root)

    def refresh(self):
        user = login.current_user
        self.name_input.text = user.get("full_name", "")
        self.phone_input.text = user.get("phone", "") or ""
        self.email_label.text = user.get("email", "")
        if user.get("avatar_path"):
            self.avatar.source = user["avatar_path"]

    def save_profile(self, *args):
        user_id = login.current_user.get("id")
        if not user_id:
            return
        database.update_profile(user_id, full_name=self.name_input.text.strip(),
                                 phone=self.phone_input.text.strip())
        login.current_user["full_name"] = self.name_input.text.strip()
        login.current_user["phone"] = self.phone_input.text.strip()

    def logout(self, *args):
        login.current_user.clear()
        self.manager.current = "login"

    def on_pre_enter(self, *args):
        self.build_ui()
        self.refresh()
