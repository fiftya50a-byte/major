"""
products.py
------------
شاشة عرض كل المنتجات (الدراجات) في شبكة، مع مربع بحث بسيط.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp

import database
from translation import tr
from screens.bike_card import BikeCard
import screens.login as login


class ProductsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical")

        self.search_input = TextInput(hint_text=tr("search"), multiline=False,
                                       size_hint=(1, None), height=dp(45))
        self.search_input.bind(text=self.on_search)

        self.grid = GridLayout(cols=2, spacing=dp(8), padding=dp(8),
                                size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.grid)

        root.add_widget(self.search_input)
        root.add_widget(scroll)
        self.add_widget(root)

    def refresh(self, filter_text=""):
        self.grid.clear_widgets()
        products = database.get_all_products()
        user_id = login.current_user.get("id")

        for p in products:
            if filter_text and filter_text.lower() not in p["name"].lower():
                continue
            card = BikeCard(product=p, user_id=user_id,
                             on_open_details=self.open_details)
            self.grid.add_widget(card)

        if not products:
            self.grid.add_widget(Label(text=tr("empty_cart"), size_hint_y=None,
                                        height=dp(60)))

    def open_details(self, product):
        reviews_screen = self.manager.get_screen("reviews")
        reviews_screen.set_product(product)
        self.manager.current = "reviews"

    def on_search(self, instance, value):
        self.refresh(filter_text=value)

    def on_pre_enter(self, *args):
        self.refresh(filter_text=self.search_input.text if hasattr(self, "search_input") else "")
