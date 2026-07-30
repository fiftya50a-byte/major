"""
translation.py
----------------
نظام ترجمة بسيط بين العربية والإنجليزية.
كل شاشة تستدعي tr("key") لعرض النص بلغة المستخدم الحالية.
اللغة تُحفظ في settings.json حتى تبقى بعد إغلاق التطبيق.
"""

import json
import os

BASE_DIR = os.path.dirname(__file__)
LOCALES_DIR = os.path.join(BASE_DIR, "locales")
SETTINGS_FILE = os.path.join(BASE_DIR, "app_settings.json")

_current_lang = "ar"
_translations = {}


def _load_language_file(lang_code):
    path = os.path.join(LOCALES_DIR, f"{lang_code}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_saved_language():
    """يُستدعى عند إقلاع التطبيق ليقرأ آخر لغة اختارها المستخدم."""
    global _current_lang
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            _current_lang = data.get("language", "ar")
    set_language(_current_lang)


def set_language(lang_code):
    """يبدّل اللغة الحالية ويحفظها، ويُعيد تحميل قاموس الترجمة."""
    global _current_lang, _translations
    _current_lang = lang_code
    _translations = _load_language_file(lang_code)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"language": lang_code}, f, ensure_ascii=False)


def get_language():
    return _current_lang


def is_rtl():
    return _current_lang == "ar"


def tr(key):
    """يرجع النص المترجم لمفتاح معيّن، أو المفتاح نفسه إن لم توجد ترجمة."""
    return _translations.get(key, key)
