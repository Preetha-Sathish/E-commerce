import sqlite3
import getpass
import os

DB = "ecommerce.db"

# ---------------------- DATABASE SETUP --------------------------

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    description TEXT
                )""")

    conn.commit()
    conn.close()

# ---------------------- USER SYSTEM -----------------------------

def register():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password))
        conn.commit()
        print("✔ Registration successful!")
    except:
        print("✖ Username already exists.")
    conn.close()

def login():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        print(f"✔ Logged in as {username}")
        return username
    else:
        print("✖ Invalid login.")
        return None

# ---------------------- PRODUCT SYSTEM --------------------------

def add_product():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    name = input("Product name: ")
    price = float(input("Price: "))
    desc = input("Description: ")

    cur.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
                (name, price, desc))
    conn.commit()
    conn.close()

    print("✔ Product added successfully!")

def list_products():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    print("\n------ PRODUCTS ------")
    for p in products:
        print(f"{p[0]}. {p[1]} - ${p[2]}\n   {p[3]}")
    print("----------------------\n")

    return products

# ---------------------- CART SYSTEM -----------------------------

cart = []

def add_to_cart():
    products = list_products()
    pid = int(input("Enter product ID to add to cart: "))

    if any(p[0] == pid for p in products):
        cart.append(pid)
        print("✔ Added to cart!")
    else:
        print("✖ Invalid product ID.")

def view_cart():
    if not cart:
        print("Cart is empty.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    print("\n----- YOUR CART -----")
    total = 0

    for pid in cart:
        cur.execute("SELECT name, price FROM products WHERE id=?", (pid,))
        item = cur.fetchone()
        if item:
            print(f"{item[0]} - ${item[1]}")
            total += item[1]

    conn.close()

    print("---------------------")
    print(f"Total: ${total}\n")

def checkout():
    if not cart:
        print("Cart empty!")
        return

    view_cart()

    confirm = input("Confirm checkout? (y/n): ").lower()
    if confirm == "y":
        cart.clear()
        print("✔ Order placed successfully!")
    else:
        print("Checkout canceled.")

# ---------------------- MAIN MENU -------------------------------

def main():
    init_db()

    while True:
        print("""
====== E-COMMERCE APP ======
1. Register
2. Login
3. Admin - Add Product
4. List Products
5. Add to Cart
6. View Cart
7. Checkout
8. Exit
""")

        choice = input("Enter choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            add_product()
        elif choice == "4":
            list_products()
        elif choice == "5":
            add_to_cart()
        elif choice == "6":
            view_cart()
        elif choice == "7":
            checkout()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
