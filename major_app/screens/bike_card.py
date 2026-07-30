"""
bike_card.py
-------------
عنصر واجهة قابل لإعادة الاستخدام يمثل "كرت" دراجة واحدة.
يُستخدم في products.py و home.py و wishlist.py.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr

PLACEHOLDER_IMAGE = "assets/bike_placeholder.png"


class BikeCard(BoxLayout):
    """
    كرت منتج يعرض الصورة، الاسم، السعر، وزرّي "أضف للسلة" و"مفضلة".

    on_open_details: دالة تُستدعى عند الضغط على الكرت لعرض التفاصيل/التقييمات
    """

    def __init__(self, product: dict, user_id=None, on_open_details=None, **kwargs):
        super().__init__(orientation="vertical", size_hint=(1, None),
                          height=dp(230), padding=dp(8), spacing=dp(4), **kwargs)
        self.product = product
        self.user_id = user_id
        self.on_open_details = on_open_details
        self.build()

    def build(self):
        image = AsyncImage(
            source=self.product.get("image_path") or PLACEHOLDER_IMAGE,
            size_hint=(1, 0.55),
        )

        name_label = Label(text=self.product.get("name", ""), bold=True,
                            size_hint=(1, 0.15), font_size="16sp")
        price_label = Label(text=f"{self.product.get('price', 0):.2f} $",
                             size_hint=(1, 0.12), font_size="14sp",
                             color=(0.2, 0.6, 1, 1))

        buttons_row = BoxLayout(size_hint=(1, 0.18), spacing=dp(6))

        cart_btn = Button(text="🛒 " + tr("add_to_cart"))
        cart_btn.bind(on_release=self.add_to_cart)

        wish_btn = Button(text="❤")
        wish_btn.bind(on_release=self.toggle_wishlist)

        buttons_row.add_widget(cart_btn)
        buttons_row.add_widget(wish_btn)

        self.add_widget(image)
        self.add_widget(name_label)
        self.add_widget(price_label)
        self.add_widget(buttons_row)

        # فتح تفاصيل المنتج عند الضغط على الصورة
        image.bind(on_touch_down=self._maybe_open_details)

    def _maybe_open_details(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.on_open_details:
            self.on_open_details(self.product)
            return True
        return False

    def add_to_cart(self, *args):
        if self.user_id:
            database.add_to_cart(self.user_id, self.product["id"])

    def toggle_wishlist(self, *args):
        if self.user_id:
            database.toggle_wishlist(self.user_id, self.product["id"])
