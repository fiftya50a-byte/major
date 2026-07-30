[app]

# اسم التطبيق كما يظهر على الهاتف
title = Major

# معرّف الحزمة (غيّر "com.majorapp" إلى نطاقك الخاص)
package.name = major
package.domain = com.majorapp

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

# رقم الإصدار
version = 1.0.0

# المكتبات المطلوبة داخل التطبيق
requirements = python3,kivy==2.3.0,plyer,kivy_garden.zbarcam,pyzbar,sqlite3,android

# الشعار وشاشة البدء (ضع الملفات داخل مجلد assets)
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png

orientation = portrait
fullscreen = 0

# الصلاحيات المطلوبة: كاميرا للماسح، إنترنت، إشعارات، تخزين
android.permissions = CAMERA, INTERNET, POST_NOTIFICATIONS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# استخدام AndroidX (مطلوب لبعض المكتبات الحديثة)
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
