"""
home.py
--------
الشاشة الرئيسية بعد تسجيل الدخول: ترحيب بالمستخدم، شريط تنقل سفلي
بسيط، وعرض لأحدث المنتجات المضافة.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr
from screens.bike_card import BikeCard
import screens.login as login


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical")

        top_bar = BoxLayout(size_hint=(1, None), height=dp(56), padding=dp(10))
        self.welcome_label = Label(text=tr("welcome_back"), font_size="18sp",
                                    bold=True, halign="left")
        top_bar.add_widget(self.welcome_label)

        self.grid = GridLayout(cols=2, spacing=dp(8), padding=dp(8),
                                size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.grid)

        nav_bar = BoxLayout(size_hint=(1, None), height=dp(56))
        nav_items = [
            ("🏠", "home"), ("🚲", "products"), ("🛒", "cart"),
            ("❤", "wishlist"), ("🔔", "notifications"), ("👤", "profile"),
        ]
        for icon, screen_name in nav_items:
            btn = Button(text=icon, font_size="20sp")
            btn.bind(on_release=lambda inst, s=screen_name: self.go_to(s))
            nav_bar.add_widget(btn)

        root.add_widget(top_bar)
        root.add_widget(scroll)
        root.add_widget(nav_bar)
        self.add_widget(root)

    def go_to(self, screen_name):
        self.manager.current = screen_name

    def refresh(self):
        name = login.current_user.get("full_name", "")
        self.welcome_label.text = f"{tr('welcome_back')}, {name} 👋"

        self.grid.clear_widgets()
        products = database.get_all_products()[:10]
        user_id = login.current_user.get("id")
        for p in products:
            self.grid.add_widget(BikeCard(product=p, user_id=user_id))

    def on_pre_enter(self, *args):
        self.build_ui()
        self.refresh()
