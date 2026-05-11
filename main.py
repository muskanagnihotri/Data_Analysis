"""Entry point for the complete e-commerce data analysis pipeline."""
import matplotlib
matplotlib.use("Agg")
import os
import sys
import pandas as pd
import analysis
import data_generator
import sql_search
import utils
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
def _rupee(value: float) -> str:
    return f"₹{value:,.2f}"
def _print_kpi_summary(df: pd.DataFrame) -> None:
    total_revenue = df["sale_amount"].sum()
    total_orders = len(df)
    unique_customers = df["customer_id"].nunique()
    average_order_value = df["sale_amount"].mean()
    return_rate = df["return_flag"].mean() * 100
    print("\nKPI Summary")
    print("-" * 60)
    print(f"Total Revenue       : {_rupee(total_revenue)}")
    print(f"Total Orders        : {total_orders:,}")
    print(f"Unique Customers    : {unique_customers:,}")
    print(f"Average Order Value : {_rupee(average_order_value)}")
    print(f"Return Rate %       : {return_rate:,.2f}%")
    print("-" * 60)
def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = data_generator.generate(n=80000)
    utils.print_numpy_stats(df["sale_amount"].to_numpy(), "Sale Amount Statistics")
    sql_search.load_to_sql()
    _print_kpi_summary(df)
    analysis.run_all_charts()
    launch_sql = input("\nLaunch SQL Search Engine? [Y/N] ").strip().upper()
    if launch_sql == "Y":
        sql_search.search_engine()
    print("\nDone! Charts in ./charts/ | DB: ecommerce.db")
if __name__ == "__main__":
    main()
