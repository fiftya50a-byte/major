"""
cart.py
--------
شاشة سلة المشتريات: عرض العناصر، حذفها، وحساب الإجمالي.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr
import screens.login as login


class CartRow(BoxLayout):
    def __init__(self, item, on_remove, **kwargs):
        super().__init__(size_hint=(1, None), height=dp(60), padding=dp(6),
                          spacing=dp(8), **kwargs)
        self.item = item
        name = f"{item['name']} x{item['quantity']}"
        price = f"{item['price'] * item['quantity']:.2f} $"

        self.add_widget(Label(text=name, size_hint=(0.6, 1)))
        self.add_widget(Label(text=price, size_hint=(0.25, 1)))

        remove_btn = Button(text="✖", size_hint=(0.15, 1))
        remove_btn.bind(on_release=lambda *_: on_remove(item["cart_id"]))
        self.add_widget(remove_btn)


class CartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None,
                                   spacing=dp(4))
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.list_box)

        self.total_label = Label(text=f"{tr('total')}: 0.00 $", size_hint=(1, 0.08),
                                  font_size="18sp", bold=True)

        checkout_btn = Button(text=tr("checkout"), size_hint=(1, 0.1),
                               background_color=(0.1, 0.6, 0.3, 1))
        checkout_btn.bind(on_release=self.checkout)

        root.add_widget(scroll)
        root.add_widget(self.total_label)
        root.add_widget(checkout_btn)
        self.add_widget(root)

    def refresh(self):
        self.list_box.clear_widgets()
        user_id = login.current_user.get("id")
        items = database.get_cart_items(user_id) if user_id else []

        if not items:
            self.list_box.add_widget(Label(text=tr("empty_cart"),
                                            size_hint_y=None, height=dp(50)))
        total = 0
        for item in items:
            total += item["price"] * item["quantity"]
            self.list_box.add_widget(CartRow(item, self.remove_item))

        self.total_label.text = f"{tr('total')}: {total:.2f} $"

    def remove_item(self, cart_id):
        database.remove_from_cart(cart_id)
        self.refresh()

    def checkout(self, *args):
        user_id = login.current_user.get("id")
        if user_id:
            database.add_notification(user_id, tr("checkout"), tr("total"))
            database.clear_cart(user_id)
            self.refresh()

    def on_pre_enter(self, *args):
        self.refresh()
