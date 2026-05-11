"""Synthetic Indian e-commerce data generator."""
import os
import numpy as np
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = "ecommerce_80k.csv"

CATEGORIES_PRODUCTS = {
    "Electronics": [
        "Smartphone",
        "Laptop",
        "Bluetooth Speaker",
        "Smartwatch",
        "Headphones",
        "Tablet",
    ],
    "Clothing": [
        "Kurta",
        "Jeans",
        "T-Shirt",
        "Saree",
        "Jacket",
        "Sneakers",
    ],
    "Home & Kitchen": [
        "Mixer Grinder",
        "Pressure Cooker",
        "Dinner Set",
        "Air Fryer",
        "Bedsheet",
        "Water Purifier",
    ],
    "Books": [
        "Fiction Novel",
        "Exam Guide",
        "Biography",
        "Cookbook",
        "Children Story Book",
        "Business Book",
    ],
    "Sports": [
        "Cricket Bat",
        "Football",
        "Yoga Mat",
        "Badminton Racket",
        "Running Shoes",
        "Fitness Band",
    ],
    "Beauty": [
        "Face Cream",
        "Lipstick",
        "Perfume",
        "Shampoo",
        "Sunscreen",
        "Hair Dryer",
    ],
    "Toys": [
        "Building Blocks",
        "Remote Car",
        "Board Game",
        "Doll Set",
        "Puzzle",
        "Soft Toy",
    ],
    "Automotive": [
        "Car Vacuum",
        "Bike Helmet",
        "Seat Cover",
        "Dash Camera",
        "Engine Oil",
        "Car Charger",
    ],
    "Grocery": [
        "Basmati Rice",
        "Atta Pack",
        "Cooking Oil",
        "Tea Pack",
        "Dry Fruits",
        "Spice Box",
    ],
    "Office": [
        "Printer",
        "Office Chair",
        "Notebook Pack",
        "Desk Lamp",
        "Pen Set",
        "Monitor Stand",
    ],
}

CITIES = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Surat",
]
CITY_REGION = {
    "Mumbai": "West",
    "Delhi": "North",
    "Bengaluru": "South",
    "Hyderabad": "South",
    "Chennai": "South",
    "Kolkata": "East",
    "Pune": "West",
    "Ahmedabad": "West",
    "Jaipur": "North",
    "Surat": "West",
}
def generate(n: int = 80000) -> pd.DataFrame:
    """Generate and save a reproducible synthetic e-commerce dataset."""
    np.random.seed(42)
    os.makedirs(DATA_DIR, exist_ok=True)
    categories = np.random.choice(list(CATEGORIES_PRODUCTS.keys()), size=n)
    product_names = [
        np.random.choice(CATEGORIES_PRODUCTS[category]) for category in categories
    ]
    cities = np.random.choice(CITIES, size=n)
    base_price = np.random.uniform(100, 80000, size=n)
    discount_pct = np.random.uniform(0.0, 0.40, size=n)
    quantity = np.random.choice(
        [1, 2, 3, 4, 5], size=n, p=[0.45, 0.25, 0.15, 0.10, 0.05]
    )
    order_dates = pd.to_datetime(
        np.random.choice(
            pd.date_range("2022-01-01", "2024-12-31", freq="D"),
            size=n,
        )
    )
    df = pd.DataFrame(
        {
            "order_id": [f"ORD{i:06d}" for i in range(1, n + 1)],
            "customer_id": [f"CUST{i:05d}" for i in np.random.randint(1, 20001, size=n)],
            "product_name": product_names,
            "category": categories,
            "city": cities,
            "region": [CITY_REGION[city] for city in cities],
            "gender": np.random.choice(["Male", "Female", "Other"], size=n),
            "age": np.clip(np.random.normal(35, 10, size=n), 18, 70).round().astype(int),
            "quantity": quantity,
            "base_price": base_price,
            "discount_pct": discount_pct,
            "sale_amount": base_price * (1 - discount_pct) * quantity,
            "payment_method": np.random.choice(
                [
                    "Credit Card",
                    "Debit Card",
                    "UPI",
                    "Net Banking",
                    "Cash on Delivery",
                    "Wallet",
                ],
                size=n,
            ),
            "rating": np.random.randint(1, 6, size=n),
            "order_date": order_dates,
            "return_flag": np.random.choice([1, 0], size=n, p=[0.08, 0.92]),
        }
    )
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.month_name()
    df["year"] = df["order_date"].dt.year
    df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
    csv_path = os.path.join(DATA_DIR, DATA_FILE)
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df):,} rows and saved dataset to {csv_path}")
    return df
if __name__ == "__main__":
    generate()
