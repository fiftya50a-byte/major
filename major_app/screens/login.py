"""
login.py
---------
شاشة تسجيل الدخول. تتحقق من المستخدم عبر database.verify_login
وتنتقل إلى الشاشة الرئيسية عند النجاح.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr

# سيتم تعيينه من main.py عند تسجيل الدخول بنجاح (معرّف المستخدم الحالي)
current_user = {}


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(14))

        title = Label(text=tr("app_name"), font_size="32sp", size_hint=(1, 0.15),
                       bold=True)
        subtitle = Label(text=tr("welcome_back"), font_size="16sp", size_hint=(1, 0.08))

        self.email_input = TextInput(hint_text=tr("email"), multiline=False,
                                      size_hint=(1, 0.09))
        self.password_input = TextInput(hint_text=tr("password"), multiline=False,
                                         password=True, size_hint=(1, 0.09))

        self.error_label = Label(text="", color=(1, 0.3, 0.3, 1), size_hint=(1, 0.08))

        login_btn = Button(text=tr("login"), size_hint=(1, 0.1),
                            background_color=(0.13, 0.13, 0.15, 1))
        login_btn.bind(on_release=self.do_login)

        goto_register_btn = Button(text=tr("no_account"), size_hint=(1, 0.08),
                                    background_color=(0, 0, 0, 0))
        goto_register_btn.bind(on_release=self.goto_register)

        root.add_widget(Label(size_hint=(1, 0.1)))
        root.add_widget(title)
        root.add_widget(subtitle)
        root.add_widget(self.email_input)
        root.add_widget(self.password_input)
        root.add_widget(self.error_label)
        root.add_widget(login_btn)
        root.add_widget(goto_register_btn)
        root.add_widget(Label(size_hint=(1, 0.2)))

        self.add_widget(root)

    def do_login(self, *args):
        global current_user
        email = self.email_input.text.strip()
        password = self.password_input.text

        if not email or not password:
            self.error_label.text = tr("email") + " / " + tr("password")
            return

        user = database.verify_login(email, password)
        if user:
            current_user.clear()
            current_user.update(user)
            self.error_label.text = ""
            self.manager.current = "home"
        else:
            self.error_label.text = "❌ " + tr("login")

    def goto_register(self, *args):
        self.manager.current = "register"

    def on_pre_enter(self, *args):
        # إعادة بناء الواجهة عند تغيير اللغة
        self.build_ui()
