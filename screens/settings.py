"""
settings.py
------------
شاشة الإعدادات: تبديل اللغة (عربي/إنجليزي) بشكل فوري ودائم.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

from translation import tr, set_language, get_language


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(14))

        title = Label(text=tr("settings"), font_size="22sp", bold=True,
                      size_hint=(1, 0.15))

        lang_label = Label(text=tr("language"), size_hint=(1, 0.1))

        lang_row = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        ar_btn = Button(text=tr("arabic"))
        ar_btn.bind(on_release=lambda *_: self.change_language("ar"))
        en_btn = Button(text=tr("english"))
        en_btn.bind(on_release=lambda *_: self.change_language("en"))
        lang_row.add_widget(ar_btn)
        lang_row.add_widget(en_btn)

        back_btn = Button(text=tr("profile"), size_hint=(1, 0.1))
        back_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "profile"))

        root.add_widget(title)
        root.add_widget(lang_label)
        root.add_widget(lang_row)
        root.add_widget(Label(size_hint=(1, 0.4)))
        root.add_widget(back_btn)

        self.add_widget(root)

    def change_language(self, lang_code):
        if get_language() != lang_code:
            set_language(lang_code)
            # إعادة بناء كل الشاشات بعد تغيير اللغة
            self.manager.rebuild_all_screens()
        self.build_ui()

    def on_pre_enter(self, *args):
        self.build_ui()
