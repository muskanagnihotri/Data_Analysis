# E-Commerce Sales Analysis
A end-to-end data analysis project built with Python — covering data generation, SQL storage, statistical analysis, and visualisation across 80,000 Data of synthetic Indian e-commerce sales data.

# Project Overview
This project simulates a real-world data analyst workflow:
Generate a large, realistic dataset using NumPy
Store and query it using SQLite (SQL)
Analyse it using Pandas
Visualise insights using Matplotlib and Seaborn
Expose an interactive SQL Search Engine via the terminal

# Dataset
The dataset is synthetically generated using NumPy — no external download required. It simulates realistic Indian e-commerce sales patterns across 3 years (2022–2024).

# Visualisations
# Chart 1 — Sales Dashboard 
6-panel overview: revenue by category, payment method share, monthly trend by year, category × city heatmap, rating distribution.
# Chart 2 — Customer Demographics 
Age distribution (histogram + KDE), average order value by gender, age vs sale amount scatter (3,000 sample).
# Chart 3 — Returns & Discounts 
Return rate % per category (horizontal bar), discount % spread per category (box plot).
# Chart 4 — Quarterly Revenue 
Bar chart of Q1–Q4 revenue per year, data pulled directly from SQLite via pd.read_sql_query.
# Chart 5 — Correlation Matrix
Seaborn heatmap showing Pearson correlation between: age, quantity, base_price, discount_pct, sale_amount, rating, return_flag.


