# Major 🚲

تطبيق بايثون (Kivy) لبيع/عرض الدراجات: تسجيل دخول، منتجات، سلة، مفضلة،
ماسح باركود، تقييمات، إشعارات، ملف شخصي، إعدادات، ودعم كامل للعربية
والإنجليزية.

## 1) هيكل المشروع

```
major_app/
├── main.py                # نقطة الدخول
├── database.py            # طبقة قاعدة البيانات SQLite
├── translation.py         # نظام الترجمة AR/EN
├── locales/
│   ├── ar.json
│   └── en.json
├── screens/
│   ├── login.py
│   ├── register.py
│   ├── home.py
│   ├── products.py
│   ├── bike_card.py
│   ├── cart.py
│   ├── wishlist.py
│   ├── scanner.py
│   ├── reviews.py
│   ├── notifications.py
│   ├── profile.py
│   └── settings.py
├── assets/                 # الشعار والصور (يمكن استبدالها)
├── requirements.txt
├── buildozer.spec
└── .github/workflows/build.yml
```

## 2) التشغيل محليًا (على الحاسوب، للتجربة السريعة)

```bash
python -m venv venv
source venv/bin/activate      # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> ملاحظة: مكتبة `kivy_garden.zbarcam` تحتاج كاميرا فعلية للعمل الكامل؛
> على الحاسوب بدون كاميرا مناسبة، استخدم خانة إدخال الباركود اليدوية
> الموجودة في شاشة الماسح كبديل مؤقت.

## 3) رفع المشروع على GitHub

```bash
git init
git add .
git commit -m "Initial commit - Major app"
git branch -M main
git remote add origin https://github.com/USERNAME/major-app.git
git push -u origin main
```

## 4) بناء تطبيق أندرويد (APK) تلقائيًا عبر GitHub Actions

الملف `.github/workflows/build.yml` جاهز مسبقًا. بمجرد الـ push إلى
`main`، سيبدأ GitHub تلقائيًا في:
1. تثبيت Buildozer وكل الاعتماديات.
2. بناء ملف APK عبر `buildozer android debug`.
3. رفع الـ APK كـ Artifact يمكنك تحميله من تبويب **Actions** في المستودع.

لتشغيله يدويًا: اذهب إلى تبويب **Actions** ثم **Build Major APK** ثم
**Run workflow**.

## 5) البناء يدويًا (على Linux/WSL)

```bash
pip install buildozer cython
buildozer android debug
# الملف الناتج: bin/major-1.0.0-arm64-v8a-debug.apk
```

## 6) الشعار والأيقونات

تم إنشاء نسخة أولية (placeholder) للشعار وشاشة البدء في مجلد `assets/`:
- `assets/icon.png` — أيقونة التطبيق (دائرة بحرف "M").
- `assets/splash.png` — شاشة البدء.
- `assets/bike_placeholder.png` — صورة افتراضية لأي منتج بدون صورة.
- `assets/avatar_placeholder.png` — صورة افتراضية للملف الشخصي.

هذه تصاميم مبدئية بسيطة لتشغيل التطبيق فورًا. يُنصح باستبدالها بتصميم
احترافي نهائي (عبر مصمم جرافيك أو أداة مثل Canva/Figma)، مع الحفاظ على
نفس الأسماء والأبعاد:
- الأيقونة: 512×512 بكسل، مربعة، خلفية شفافة أو دائرية.
- شاشة البدء: 720×1280 بكسل.

## 7) إضافة منتجات تجريبية لقاعدة البيانات

يمكنك تشغيل هذا الكود مرة واحدة (مثلاً من ملف `seed.py` منفصل) لإضافة
دراجات تجريبية:

```python
import database
database.init_db()
database.add_product("Trek Marlin 7", price=899.99, brand="Trek",
                      category="Mountain", barcode="1111", stock=5)
database.add_product("Cannondale Quick 3", price=650.0, brand="Cannondale",
                      category="Road", barcode="2222", stock=3)
```

## 8) الترجمة

كل النصوص تُقرأ عبر `tr("key")` من `locales/ar.json` و `locales/en.json`.
لإضافة نص جديد: أضف نفس المفتاح (`key`) في كلا الملفين بالترجمة المناسبة.
تبديل اللغة يتم من شاشة **الإعدادات** ويُحفظ تلقائيًا في `app_settings.json`.
