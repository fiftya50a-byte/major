"""
scanner.py
-----------
شاشة مسح الباركود لإيجاد منتج بسرعة عبر كاميرا الهاتف.
تعتمد على مكتبة kivy_garden.zbarcam (تُضاف في requirements/buildozer).
في حال عدم توفر الكاميرا (مثلاً عند التجربة على الحاسوب) تظهر خانة
إدخال يدوي للباركود كبديل.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp

import database
from translation import tr

try:
    from kivy_garden.zbarcam import ZBarCam
    ZBAR_AVAILABLE = True
except Exception:
    ZBAR_AVAILABLE = False


class ScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zbarcam = None
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))

        title = Label(text=tr("scan_barcode"), font_size="20sp", bold=True,
                      size_hint=(1, 0.1))
        root.add_widget(title)

        if ZBAR_AVAILABLE:
            self.zbarcam = ZBarCam(size_hint=(1, 0.6))
            self.zbarcam.bind(symbols=self.on_symbols)
            root.add_widget(self.zbarcam)
        else:
            root.add_widget(Label(text="📷 " + tr("scan_barcode"),
                                   size_hint=(1, 0.3)))

        self.manual_input = TextInput(hint_text="Barcode / QR", multiline=False,
                                       size_hint=(1, 0.1))
        search_btn = Button(text=tr("search"), size_hint=(1, 0.1))
        search_btn.bind(on_release=self.search_manual)

        self.result_label = Label(text="", size_hint=(1, 0.2))

        root.add_widget(self.manual_input)
        root.add_widget(search_btn)
        root.add_widget(self.result_label)
        self.add_widget(root)

    def on_symbols(self, instance, symbols):
        if symbols:
            code = symbols[0].data.decode("utf-8")
            self.lookup(code)

    def search_manual(self, *args):
        code = self.manual_input.text.strip()
        if code:
            self.lookup(code)

    def lookup(self, code):
        product = database.get_product_by_barcode(code)
        if product:
            self.result_label.text = f"✅ {product['name']} - {product['price']} $"
            reviews_screen = self.manager.get_screen("reviews")
            reviews_screen.set_product(product)
            self.manager.current = "reviews"
        else:
            self.result_label.text = "❌ " + tr("empty_cart")

    def on_leave(self, *args):
        if self.zbarcam:
            self.zbarcam.stop()

    def on_pre_enter(self, *args):
        if self.zbarcam:
            self.zbarcam.play = True
