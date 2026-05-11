"""Utility helpers for numeric summaries."""
import sys
import numpy as np
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
def print_numpy_stats(arr: np.ndarray, label: str) -> None:
    """Print descriptive statistics for a numeric NumPy array."""
    values = np.asarray(arr, dtype=float)
    mean = np.mean(values)
    median = np.median(values)
    std = np.std(values)
    centered = values - mean
    skewness = np.mean(centered**3) / (std**3) if std else 0.0
    kurtosis = np.mean(centered**4) / (std**4) - 3 if std else 0.0
    stats = {
        "Mean": mean,
        "Median": median,
        "Std": std,
        "Variance": np.var(values),
        "Min": np.min(values),
        "Max": np.max(values),
        "25th Percentile": np.percentile(values, 25),
        "75th Percentile": np.percentile(values, 75),
        "99th Percentile": np.percentile(values, 99),
        "Skewness": skewness,
        "Kurtosis": kurtosis,
    }
    width = 58
    print("-" * width)
    print(f"{label.upper():^{width}}")
    print("-" * width)
    for stat_name, value in stats.items():
        print(f"{stat_name:<22}: ₹{value:,.2f}")
    print("-" * width)
