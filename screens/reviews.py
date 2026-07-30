"""
reviews.py
-----------
شاشة تفاصيل المنتج وتقييماته: تعرض معلومات المنتج، قائمة التقييمات
السابقة، ونموذجًا لإضافة تقييم جديد (نجوم 1-5 + تعليق).
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.metrics import dp

import database
from translation import tr
import screens.login as login


class ReviewRow(BoxLayout):
    def __init__(self, review, **kwargs):
        super().__init__(orientation="vertical", size_hint=(1, None), height=dp(70),
                          padding=dp(6), **kwargs)
        stars = "⭐" * review["rating"]
        self.add_widget(Label(text=f"{review['full_name']}  {stars}",
                               bold=True, size_hint=(1, 0.5), halign="left"))
        self.add_widget(Label(text=review.get("comment") or "",
                               size_hint=(1, 0.5)))


class ReviewsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product = None
        self.selected_rating = 5
        self.build_ui()

    def set_product(self, product):
        self.product = product
        self.refresh()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        self.image = AsyncImage(source="assets/bike_placeholder.png",
                                 size_hint=(1, 0.3))
        self.name_label = Label(text="", font_size="20sp", bold=True,
                                 size_hint=(1, 0.08))
        self.price_label = Label(text="", size_hint=(1, 0.06))

        self.reviews_box = BoxLayout(orientation="vertical", size_hint_y=None,
                                      spacing=dp(4))
        self.reviews_box.bind(minimum_height=self.reviews_box.setter("height"))
        scroll = ScrollView(size_hint=(1, 0.3))
        scroll.add_widget(self.reviews_box)

        stars_row = BoxLayout(size_hint=(1, 0.08))
        self.star_buttons = []
        for i in range(1, 6):
            b = Button(text="★")
            b.bind(on_release=lambda inst, n=i: self.set_rating(n))
            stars_row.add_widget(b)
            self.star_buttons.append(b)

        self.comment_input = TextInput(hint_text=tr("write_review"),
                                        multiline=True, size_hint=(1, 0.12))
        submit_btn = Button(text=tr("submit"), size_hint=(1, 0.08))
        submit_btn.bind(on_release=self.submit_review)

        root.add_widget(self.image)
        root.add_widget(self.name_label)
        root.add_widget(self.price_label)
        root.add_widget(scroll)
        root.add_widget(stars_row)
        root.add_widget(self.comment_input)
        root.add_widget(submit_btn)

        self.add_widget(root)
        self.set_rating(5)

    def set_rating(self, n):
        self.selected_rating = n
        for i, b in enumerate(self.star_buttons, start=1):
            b.text = "★" if i <= n else "☆"

    def refresh(self):
        if not self.product:
            return
        self.image.source = self.product.get("image_path") or "assets/bike_placeholder.png"
        self.name_label.text = self.product.get("name", "")
        self.price_label.text = f"{self.product.get('price', 0):.2f} $"

        self.reviews_box.clear_widgets()
        reviews = database.get_reviews_for_product(self.product["id"])
        if not reviews:
            self.reviews_box.add_widget(Label(text=tr("no_notifications"),
                                               size_hint_y=None, height=dp(40)))
        for r in reviews:
            self.reviews_box.add_widget(ReviewRow(r))

    def submit_review(self, *args):
        user_id = login.current_user.get("id")
        if user_id and self.product:
            database.add_review(user_id, self.product["id"], self.selected_rating,
                                 self.comment_input.text.strip())
            self.comment_input.text = ""
            self.refresh()

    def on_pre_enter(self, *args):
        self.refresh()
