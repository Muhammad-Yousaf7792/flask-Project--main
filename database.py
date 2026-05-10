import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# ------------------------
# Connect to Database
# ------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print("❌ Error connecting to MySQL:", e)
        return None

# ------------------------
# Insert Product (Duplicate-safe)
# ------------------------
def insert_product(name, url, price):
    db = connect_db()
    if db is None:
        print("❌ Database connection failed. Product not inserted.")
        return

    try:
        cursor = db.cursor()
        # Duplicate check by URL
        cursor.execute("SELECT id FROM products WHERE url=%s", (url,))
        result = cursor.fetchone()
        if result:
            print("⚠ Product already exists. Skipping insert.")
            return

        sql = "INSERT INTO products (name, url, price) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, url, price))
        db.commit()
        print(f"✅ Product inserted: {name} | {price}")

    except Error as e:
        print("❌ Error inserting product:", e)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# ------------------------
# Get all products
# ------------------------
def get_products():
    db = connect_db()
    if db is None:
        print("❌ Cannot fetch products.")
        return []

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        data = cursor.fetchall()
        return data
    except Error as e:
        print("❌ Error fetching products:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# ------------------------
# Get product ID by URL
# ------------------------
def get_product_id_by_url(url):
    db = connect_db()
    if db is None:
        return None

    try:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM products WHERE url=%s", (url,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# ------------------------
# Insert Price History
# ------------------------
def insert_price_history(product_id, price):
    db = connect_db()
    if db is None:
        return
    try:
        cursor = db.cursor()
        sql = "INSERT INTO price_history (product_id, price) VALUES (%s, %s)"
        cursor.execute(sql, (product_id, price))
        db.commit()
    except Error as e:
        print("❌ Error inserting price history:", e)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# ------------------------
# Get Price History
# ------------------------
def get_price_history(product_id):
    db = connect_db()
    if db is None:
        return []

    try:
        cursor = db.cursor(dictionary=True)
        sql = "SELECT price, created_at FROM price_history WHERE product_id=%s ORDER BY created_at"
        cursor.execute(sql, (product_id,))
        data = cursor.fetchall()
        return data
    except Error as e:
        print("❌ Error fetching price history:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()