"""
database.py
------------
طبقة قاعدة البيانات الموحّدة لتطبيق Major.
تستخدم SQLite (ملف محلي) وتوفر دوال جاهزة لكل الشاشات:
المستخدمين، المنتجات (الدراجات)، السلة، المفضلة، التقييمات، الإشعارات.
"""

import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "major.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    """ينشئ كل الجداول إن لم تكن موجودة. يُستدعى مرة واحدة عند إقلاع التطبيق."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            avatar_path TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            price REAL NOT NULL,
            description TEXT,
            image_path TEXT,
            barcode TEXT,
            stock INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            added_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(user_id, product_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ---------------- Users ----------------

def create_user(full_name, email, password, phone=None):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (full_name, email, phone, password_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (full_name, email.lower().strip(), phone, hash_password(password),
             datetime.now().isoformat()),
        )
        conn.commit()
        return True, "تم إنشاء الحساب بنجاح"
    except sqlite3.IntegrityError:
        return False, "هذا البريد الإلكتروني مستخدم بالفعل"
    finally:
        conn.close()


def verify_login(email, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.lower().strip(),)
    ).fetchone()
    conn.close()
    if row and row["password_hash"] == hash_password(password):
        return dict(row)
    return None


def update_profile(user_id, full_name=None, phone=None, avatar_path=None):
    conn = get_connection()
    fields, values = [], []
    if full_name is not None:
        fields.append("full_name = ?"); values.append(full_name)
    if phone is not None:
        fields.append("phone = ?"); values.append(phone)
    if avatar_path is not None:
        fields.append("avatar_path = ?"); values.append(avatar_path)
    if fields:
        values.append(user_id)
        conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    conn.close()


# ---------------- Products ----------------

def add_product(name, price, brand=None, category=None, description=None,
                 image_path=None, barcode=None, stock=0):
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, brand, category, price, description, "
        "image_path, barcode, stock, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (name, brand, category, price, description, image_path, barcode,
         stock, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_all_products(category=None):
    conn = get_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY id DESC", (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_product_by_barcode(barcode):
    conn = get_connection()
    row = conn.execute("SELECT * FROM products WHERE barcode = ?", (barcode,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_product_by_id(product_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ---------------- Cart ----------------

def add_to_cart(user_id, product_id, quantity=1):
    conn = get_connection()
    existing = conn.execute(
        "SELECT * FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE cart SET quantity = quantity + ? WHERE id = ?",
            (quantity, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?,?,?)",
            (user_id, product_id, quantity),
        )
    conn.commit()
    conn.close()


def get_cart_items(user_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT cart.id AS cart_id, cart.quantity, products.*
        FROM cart JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_from_cart(cart_id):
    conn = get_connection()
    conn.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()


def clear_cart(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ---------------- Wishlist ----------------

def toggle_wishlist(user_id, product_id):
    """يضيف المنتج للمفضلة أو يزيله إن كان موجودًا. يرجع True إن أُضيف."""
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM wishlist WHERE user_id=? AND product_id=?",
        (user_id, product_id),
    ).fetchone()
    if existing:
        conn.execute("DELETE FROM wishlist WHERE id = ?", (existing["id"],))
        conn.commit(); conn.close()
        return False
    conn.execute(
        "INSERT INTO wishlist (user_id, product_id, added_at) VALUES (?,?,?)",
        (user_id, product_id, datetime.now().isoformat()),
    )
    conn.commit(); conn.close()
    return True


def get_wishlist(user_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT wishlist.id AS wishlist_id, products.*
        FROM wishlist JOIN products ON wishlist.product_id = products.id
        WHERE wishlist.user_id = ?
        ORDER BY wishlist.added_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------- Reviews ----------------

def add_review(user_id, product_id, rating, comment=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO reviews (user_id, product_id, rating, comment, created_at) "
        "VALUES (?,?,?,?,?)",
        (user_id, product_id, rating, comment, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_reviews_for_product(product_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT reviews.*, users.full_name
        FROM reviews JOIN users ON reviews.user_id = users.id
        WHERE product_id = ?
        ORDER BY reviews.created_at DESC
    """, (product_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------- Notifications ----------------

def add_notification(user_id, title, body=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO notifications (user_id, title, body, created_at) VALUES (?,?,?,?)",
        (user_id, title, body, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_notifications(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_notification_read(notification_id):
    conn = get_connection()
    conn.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()
