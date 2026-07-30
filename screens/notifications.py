"""
notifications.py
------------------
شاشة الإشعارات داخل التطبيق، بالإضافة إلى دالة مساعدة لإرسال إشعار
نظام حقيقي (push محلي) عبر مكتبة plyer، تعمل على أندرويد/iOS.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp

import database
from translation import tr
import screens.login as login

try:
    from plyer import notification as system_notification
except Exception:
    system_notification = None


def send_system_notification(title, message):
    """يعرض إشعار نظام حقيقي في شريط التنبيهات (يتطلب plyer + أندرويد)."""
    if system_notification:
        try:
            system_notification.notify(title=title, message=message,
                                        app_name="Major", timeout=6)
        except Exception:
            pass


class NotificationRow(BoxLayout):
    def __init__(self, notif, **kwargs):
        super().__init__(orientation="vertical", size_hint=(1, None), height=dp(64),
                          padding=dp(8), **kwargs)
        weight = "bold" if not notif["is_read"] else "normal"
        self.add_widget(Label(text=notif["title"], bold=(weight == "bold"),
                               size_hint=(1, 0.6), halign="left"))
        self.add_widget(Label(text=notif.get("body") or "", size_hint=(1, 0.4)))


class NotificationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        self.box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4),
                              padding=dp(8))
        self.box.bind(minimum_height=self.box.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.box)
        self.add_widget(scroll)

    def refresh(self):
        self.box.clear_widgets()
        user_id = login.current_user.get("id")
        notifs = database.get_notifications(user_id) if user_id else []

        if not notifs:
            self.box.add_widget(Label(text=tr("no_notifications"),
                                       size_hint_y=None, height=dp(50)))
        for n in notifs:
            self.box.add_widget(NotificationRow(n))
            if not n["is_read"]:
                database.mark_notification_read(n["id"])

    def on_pre_enter(self, *args):
        self.refresh()
