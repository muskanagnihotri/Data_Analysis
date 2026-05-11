"""SQLite loader and interactive SQL search engine."""
import os
import sqlite3
import sys
import numpy as np
import pandas as pd
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "ecommerce_80k.csv")
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")
TABLE_NAME = "orders"
def load_to_sql() -> None:
    """Load the generated CSV into SQLite and create search indexes."""
    np.random.seed(42)
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_category ON {TABLE_NAME}(category)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_city ON {TABLE_NAME}(city)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_orders_order_date ON {TABLE_NAME}(order_date)")
    print(f"Loaded {len(df):,} rows into {DB_PATH} table '{TABLE_NAME}'")
BUILT_IN_QUERIES = {
    "1": (
        "Top 10 products by total revenue",
        """
        SELECT product_name, category, SUM(sale_amount) AS total_revenue
        FROM orders
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT 10;
        """,
    ),
    "2": (
        "Sales by region and category",
        """
        SELECT region, category, SUM(sale_amount) AS total_revenue, COUNT(*) AS orders
        FROM orders
        GROUP BY region, category
        ORDER BY region, total_revenue DESC;
        """,
    ),
    "3": (
        "Monthly revenue trend (grouped by year and month)",
        """
        SELECT year, month, SUM(sale_amount) AS total_revenue
        FROM orders
        GROUP BY year, month
        ORDER BY year, month;
        """,
    ),
    "4": (
        "Customer age group analysis",
        """
        SELECT
            CASE
                WHEN age BETWEEN 18 AND 24 THEN '18-24'
                WHEN age BETWEEN 25 AND 34 THEN '25-34'
                WHEN age BETWEEN 35 AND 44 THEN '35-44'
                WHEN age BETWEEN 45 AND 54 THEN '45-54'
                ELSE '55+'
            END AS age_group,
            COUNT(*) AS orders,
            SUM(sale_amount) AS total_revenue,
            AVG(sale_amount) AS avg_order_value
        FROM orders
        GROUP BY age_group
        ORDER BY age_group;
        """,
    ),
    "5": (
        "Payment method popularity with avg discount",
        """
        SELECT payment_method, COUNT(*) AS orders, AVG(discount_pct) AS avg_discount
        FROM orders
        GROUP BY payment_method
        ORDER BY orders DESC;
        """,
    ),
    "6": (
        "High-value orders where sale_amount > 50000",
        """
        SELECT order_id, customer_id, product_name, category, city, sale_amount
        FROM orders
        WHERE sale_amount > 50000
        ORDER BY sale_amount DESC;
        """,
    ),
    "7": (
        "Return rate percentage by category",
        """
        SELECT category, AVG(return_flag) * 100 AS return_rate_pct
        FROM orders
        GROUP BY category
        ORDER BY return_rate_pct DESC;
        """,
    ),
    "8": (
        "Top cities by total revenue",
        """
        SELECT city, region, SUM(sale_amount) AS total_revenue, COUNT(*) AS orders
        FROM orders
        GROUP BY city, region
        ORDER BY total_revenue DESC;
        """,
    ),
    "9": (
        "Best month for each category using SQL RANK() window function",
        """
        WITH monthly_category AS (
            SELECT category, year, month, SUM(sale_amount) AS total_revenue
            FROM orders
            GROUP BY category, year, month
        ),
        ranked AS (
            SELECT
                category,
                year,
                month,
                total_revenue,
                RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS revenue_rank
            FROM monthly_category
        )
        SELECT category, year, month, total_revenue
        FROM ranked
        WHERE revenue_rank = 1
        ORDER BY category;
        """,
    ),
    "10": (
        "Discount bucket vs average sale amount",
        """
        SELECT
            CASE
                WHEN discount_pct < 0.10 THEN '0-10%'
                WHEN discount_pct < 0.20 THEN '10-20%'
                WHEN discount_pct < 0.30 THEN '20-30%'
                ELSE '30-40%'
            END AS discount_bucket,
            COUNT(*) AS orders,
            AVG(sale_amount) AS avg_sale_amount
        FROM orders
        GROUP BY discount_bucket
        ORDER BY discount_bucket;
        """,
    ),
}
def _format_currency_columns(df: pd.DataFrame) -> pd.DataFrame:
    formatted = df.copy()
    for column in formatted.columns:
        if any(token in column.lower() for token in ["revenue", "amount", "value"]):
            formatted[column] = formatted[column].map(lambda value: f"₹{value:,.2f}")
        elif "discount" in column.lower() or "rate" in column.lower():
            formatted[column] = formatted[column].map(lambda value: f"{value:,.2f}")
    return formatted
def run_query(query: str) -> pd.DataFrame:
    """Run a SQL query against the ecommerce SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)
def search_engine() -> None:
    """Run an interactive terminal SQL search engine."""
    np.random.seed(42)
    print("\nSQL Search Engine")
    print("-" * 60)
    while True:
        for key, (title, _) in BUILT_IN_QUERIES.items():
            print(f"{key}. {title}")
        print("C. Custom SQL input")
        print("Q. Quit")

        choice = input("\nChoose an option: ").strip().upper()
        if choice == "Q":
            print("Exiting SQL Search Engine.")
            break
        if choice == "C":
            query = input("Enter SQL query: ").strip()
            title = "Custom SQL Results"
        elif choice in BUILT_IN_QUERIES:
            title, query = BUILT_IN_QUERIES[choice]
        else:
            print("Invalid option. Try again.\n")
            continue
        try:
            result = run_query(query)
            print(f"\n{title}")
            print("-" * 60)
            print(_format_currency_columns(result).to_string(index=False))
            print()
        except Exception as exc:
            print(f"SQL error: {exc}\n")
if __name__ == "__main__":
    load_to_sql()
    search_engine()
