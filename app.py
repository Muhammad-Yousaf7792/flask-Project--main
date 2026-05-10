from flask import Flask, render_template, request, redirect, url_for
from scraper_test import scrape_product
from database import insert_product, get_products, get_product_id_by_url, get_price_history, insert_price_history

app = Flask(__name__)

# ------------------------
# Home route: Add / List Products
# ------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Scrape product from URL
            product = scrape_product(url)
            if product:
                name, price = product

                # Check if product already exists using URL
                product_id = get_product_id_by_url(url)

                # Insert product if not exists
                if not product_id:
                    insert_product(name, url, price)
                    product_id = get_product_id_by_url(url)
                    print(f"✅ New product added: {name} | {price}")
                else:
                    print(f"⚠ Product already exists. Skipping insert: {name}")

                # Insert price history
                if product_id:
                    insert_price_history(product_id, price)

        return redirect(url_for("home"))

    # Fetch all products
    products = get_products()
    return render_template("index.html", products=products)

# ------------------------
# History route: Show Price History
# ------------------------
@app.route("/history/<int:product_id>")
def history(product_id):
    history_data = get_price_history(product_id)

    # Prepare lists
    dates = [row["created_at"].strftime("%Y-%m-%d") for row in history_data]
    prices = [row["price"].replace("Rs. ", "") for row in history_data]

    # Zip into pairs to fix Jinja2 zip issue
    date_price_pairs = list(zip(dates, prices))

    return render_template("history.html", date_price_pairs=date_price_pairs)

# ------------------------
# Run Flask app
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)