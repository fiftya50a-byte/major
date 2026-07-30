"""
wishlist.py
------------
شاشة المفضلة: تعرض المنتجات التي أضافها المستخدم للمفضلة.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp

import database
from translation import tr
from screens.bike_card import BikeCard
import screens.login as login


class WishlistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        self.grid = GridLayout(cols=2, spacing=dp(8), padding=dp(8),
                                size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

    def refresh(self):
        self.grid.clear_widgets()
        user_id = login.current_user.get("id")
        items = database.get_wishlist(user_id) if user_id else []

        if not items:
            self.grid.add_widget(Label(text=tr("empty_wishlist"),
                                        size_hint_y=None, height=dp(60)))
        for p in items:
            self.grid.add_widget(BikeCard(product=p, user_id=user_id))

    def on_pre_enter(self, *args):
        self.refresh()
