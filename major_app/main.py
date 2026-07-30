"""
main.py
--------
نقطة الدخول الرئيسية لتطبيق Major.
يُنشئ ScreenManager ويسجّل كل الشاشات، ويهيّئ قاعدة البيانات واللغة
عند الإقلاع.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

import database
import translation

from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.home import HomeScreen
from screens.products import ProductsScreen
from screens.cart import CartScreen
from screens.wishlist import WishlistScreen
from screens.scanner import ScannerScreen
from screens.reviews import ReviewsScreen
from screens.notifications import NotificationsScreen
from screens.profile import ProfileScreen
from screens.settings import SettingsScreen


class MajorScreenManager(ScreenManager):
    def rebuild_all_screens(self):
        """يُعاد بناء كل شاشة بعد تبديل اللغة كي تُحدَّث النصوص فورًا."""
        for screen in self.screens:
            if hasattr(screen, "build_ui"):
                screen.build_ui()


class MajorApp(App):
    title = "Major"

    def build(self):
        Window.clearcolor = (0.97, 0.97, 0.98, 1)

        # 1) تهيئة قاعدة البيانات
        database.init_db()

        # 2) تحميل آخر لغة محفوظة (عربي افتراضيًا)
        translation.load_saved_language()

        # 3) بناء مدير الشاشات وتسجيل كل الشاشات
        sm = MajorScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProductsScreen(name="products"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(WishlistScreen(name="wishlist"))
        sm.add_widget(ScannerScreen(name="scanner"))
        sm.add_widget(ReviewsScreen(name="reviews"))
        sm.add_widget(NotificationsScreen(name="notifications"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(SettingsScreen(name="settings"))

        sm.current = "login"
        return sm


if __name__ == "__main__":
    MajorApp().run()
