"""Chart generation for the e-commerce analysis project."""
import os
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
np.random.seed(42)
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams["figure.dpi"] = 130
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "ecommerce_80k.csv")
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
def _load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["order_date"])
def _save_chart(fig: plt.Figure, filename: str, apply_tight_layout: bool = True) -> str:
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, filename)
    if apply_tight_layout:
        fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved chart: {path}")
    return path
def _rupee_millions(value: float) -> str:
    return f"₹{value:,.1f}M"
def _chart_dashboard(df: pd.DataFrame) -> str:
    fig = plt.figure(figsize=(22, 18))
    gs = GridSpec(3, 3, figure=fig, hspace=0.38, wspace=0.25)
    ax1 = fig.add_subplot(gs[0, :2])
    category_revenue = (
        df.groupby("category")["sale_amount"].sum().sort_values() / 1_000_000
    )
    sns.barplot(x=category_revenue.values, y=category_revenue.index, ax=ax1)
    ax1.set_title("Revenue by Category")
    ax1.set_xlabel("Revenue (₹ Millions)")
    ax1.set_ylabel("Category")
    ax1.bar_label(ax1.containers[0], labels=[_rupee_millions(v) for v in category_revenue.values], padding=4)
    ax2 = fig.add_subplot(gs[0, 2])
    payment_share = df["payment_method"].value_counts()
    ax2.pie(payment_share.values, labels=payment_share.index, autopct="%1.1f%%", startangle=90)
    ax2.set_title("Payment Method Share")
    ax3 = fig.add_subplot(gs[1, :])
    monthly = (
        df.groupby(["year", "month"], as_index=False)["sale_amount"].sum()
        .assign(revenue_m=lambda data: data["sale_amount"] / 1_000_000)
    )
    sns.lineplot(data=monthly, x="month", y="revenue_m", hue="year", marker="o", ax=ax3)
    ax3.set_title("Monthly Revenue Trend")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Revenue (₹ Millions)")
    ax3.set_xticks(range(1, 13))
    ax4 = fig.add_subplot(gs[2, :2])
    heatmap_data = (
        df.pivot_table(index="category", columns="city", values="sale_amount", aggfunc="sum")
        / 1_000_000
    )
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax4)
    ax4.set_title("Revenue (₹M) by Category and City")
    ax4.set_xlabel("City")
    ax4.set_ylabel("Category")
    ax5 = fig.add_subplot(gs[2, 2])
    sns.countplot(data=df, x="rating", ax=ax5)
    ax5.set_title("Star Rating Distribution")
    ax5.set_xlabel("Rating")
    ax5.set_ylabel("Orders")
    return _save_chart(fig, "01_dashboard.png", apply_tight_layout=False)

def _chart_demographics(df: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(data=df, x="age", kde=True, bins=30, ax=axes[0])
    axes[0].set_title("Age Distribution")
    gender_aov = df.groupby("gender", as_index=False)["sale_amount"].mean()
    sns.barplot(data=gender_aov, x="gender", y="sale_amount", ax=axes[1])
    axes[1].set_title("Average Order Value by Gender")
    axes[1].set_ylabel("AOV (₹)")
    axes[1].bar_label(axes[1].containers[0], labels=[f"₹{v:,.0f}" for v in gender_aov["sale_amount"]], padding=3)
    sample = df.sample(3000, random_state=42)
    sns.scatterplot(
        data=sample,
        x="age",
        y="sale_amount",
        hue="category",
        alpha=0.55,
        s=18,
        ax=axes[2],
    )
    axes[2].set_title("Age vs Sale Amount")
    axes[2].set_ylabel("Sale Amount (₹)")
    axes[2].legend(fontsize=7, loc="upper right")
    return _save_chart(fig, "02_demographics.png")
def _chart_returns_discounts(df: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    return_rate = (
        df.groupby("category")["return_flag"].mean().mul(100).sort_values().reset_index()
    )
    sns.barplot(data=return_rate, x="return_flag", y="category", ax=axes[0])
    axes[0].set_title("Return Rate by Category")
    axes[0].set_xlabel("Return Rate (%)")
    axes[0].set_ylabel("Category")
    sns.boxplot(data=df, x="category", y="discount_pct", ax=axes[1])
    axes[1].set_title("Discount Distribution by Category")
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Discount %")
    axes[1].tick_params(axis="x", rotation=45)
    return _save_chart(fig, "03_returns_discounts.png")
def _chart_quarterly_revenue() -> str:
    query = """
    SELECT year, quarter, SUM(sale_amount) AS revenue
    FROM orders
    GROUP BY year, quarter
    ORDER BY year, quarter;
    """
    with sqlite3.connect(DB_PATH) as conn:
        quarterly = pd.read_sql_query(query, conn)
    quarterly["label"] = quarterly["year"].astype(str) + " " + quarterly["quarter"]
    quarterly["revenue_m"] = quarterly["revenue"] / 1_000_000
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.barplot(data=quarterly, x="label", y="revenue_m", ax=ax)
    ax.set_title("Quarterly Revenue")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Revenue (₹ Millions)")
    ax.tick_params(axis="x", rotation=30)
    ax.bar_label(ax.containers[0], labels=[_rupee_millions(v) for v in quarterly["revenue_m"]], padding=3)
    return _save_chart(fig, "04_quarterly_revenue.png")
def _chart_correlation(df: pd.DataFrame) -> str:
    columns = [
        "age",
        "quantity",
        "base_price",
        "discount_pct",
        "sale_amount",
        "rating",
        "return_flag",
    ]
    corr = df[columns].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Matrix")
    return _save_chart(fig, "05_correlation.png")
def run_all_charts() -> list[str]:
    """Generate all five required chart PNG files."""
    np.random.seed(42)
    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = _load_data()
    return [
        _chart_dashboard(df),
        _chart_demographics(df),
        _chart_returns_discounts(df),
        _chart_quarterly_revenue(),
        _chart_correlation(df),
    ]
if __name__ == "__main__":
    run_all_charts()
