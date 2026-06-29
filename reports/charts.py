import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for server-side rendering
import matplotlib.pyplot as plt
import os
from typing import Dict, Any


def generate_category_pie_chart(category_distribution: Dict[str, float], output_path: str) -> str:
    """Renders expense category distribution as a pie chart image."""
    if not category_distribution:
        return ""

    labels = list(category_distribution.keys())
    values = list(category_distribution.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.tight_layout()

    file_path = os.path.join(output_path, "category_distribution.png")
    plt.savefig(file_path)
    plt.close()
    return file_path


def generate_monthly_trend_chart(monthly_trend: Dict[str, float], output_path: str) -> str:
    """Renders monthly spending trend as a line chart."""
    if not monthly_trend:
        return ""

    months = list(monthly_trend.keys())
    amounts = list(monthly_trend.values())

    plt.figure(figsize=(8, 4))
    plt.plot(months, amounts, marker="o", linewidth=2)
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=45)
    plt.tight_layout()

    file_path = os.path.join(output_path, "monthly_trend.png")
    plt.savefig(file_path)
    plt.close()
    return file_path


def generate_budget_variance_chart(variance: Dict[str, Dict[str, Any]], output_path: str) -> str:
    """Renders planned vs actual spend as a grouped bar chart."""
    if not variance:
        return ""

    categories = list(variance.keys())
    planned = [variance[c]["planned"] for c in categories]
    actual = [variance[c]["actual"] for c in categories]

    x = range(len(categories))
    width = 0.35

    plt.figure(figsize=(8, 4))
    plt.bar([i - width / 2 for i in x], planned, width=width, label="Planned")
    plt.bar([i + width / 2 for i in x], actual, width=width, label="Actual")
    plt.xticks(list(x), categories, rotation=45)
    plt.title("Budget: Planned vs Actual")
    plt.legend()
    plt.tight_layout()

    file_path = os.path.join(output_path, "budget_variance.png")
    plt.savefig(file_path)
    plt.close()
    return file_path


def generate_portfolio_allocation_chart(sector_allocation: Dict[str, float], output_path: str) -> str:
    """Renders investment sector allocation as a pie chart."""
    if not sector_allocation:
        return ""

    labels = list(sector_allocation.keys())
    values = list(sector_allocation.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Portfolio Sector Allocation")
    plt.tight_layout()

    file_path = os.path.join(output_path, "portfolio_allocation.png")
    plt.savefig(file_path)
    plt.close()
    return file_path