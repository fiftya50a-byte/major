"""
register.py
------------
شاشة إنشاء حساب جديد. تتحقق من تطابق كلمتي المرور ثم تنشئ المستخدم
عبر database.create_user.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(12))

        title = Label(text=tr("register"), font_size="28sp", size_hint=(1, 0.12),
                      bold=True)
        subtitle = Label(text=tr("create_account_msg"), font_size="14sp",
                          size_hint=(1, 0.07))

        self.name_input = TextInput(hint_text=tr("full_name"), multiline=False,
                                     size_hint=(1, 0.09))
        self.email_input = TextInput(hint_text=tr("email"), multiline=False,
                                      size_hint=(1, 0.09))
        self.phone_input = TextInput(hint_text=tr("phone"), multiline=False,
                                      size_hint=(1, 0.09))
        self.password_input = TextInput(hint_text=tr("password"), multiline=False,
                                         password=True, size_hint=(1, 0.09))
        self.confirm_input = TextInput(hint_text=tr("confirm_password"),
                                        multiline=False, password=True,
                                        size_hint=(1, 0.09))

        self.error_label = Label(text="", color=(1, 0.3, 0.3, 1), size_hint=(1, 0.07))

        register_btn = Button(text=tr("register"), size_hint=(1, 0.1),
                               background_color=(0.13, 0.13, 0.15, 1))
        register_btn.bind(on_release=self.do_register)

        goto_login_btn = Button(text=tr("have_account"), size_hint=(1, 0.07),
                                 background_color=(0, 0, 0, 0))
        goto_login_btn.bind(on_release=self.goto_login)

        for w in (title, subtitle, self.name_input, self.email_input,
                  self.phone_input, self.password_input, self.confirm_input,
                  self.error_label, register_btn, goto_login_btn):
            root.add_widget(w)

        self.add_widget(root)

    def do_register(self, *args):
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        password = self.password_input.text
        confirm = self.confirm_input.text

        if not name or not email or not password:
            self.error_label.text = "⚠ " + tr("full_name")
            return
        if password != confirm:
            self.error_label.text = "⚠ " + tr("confirm_password")
            return

        ok, message = database.create_user(name, email, password, phone)
        self.error_label.color = (0.2, 0.8, 0.2, 1) if ok else (1, 0.3, 0.3, 1)
        self.error_label.text = message

        if ok:
            self.manager.current = "login"

    def goto_login(self, *args):
        self.manager.current = "login"

    def on_pre_enter(self, *args):
        self.build_ui()
