import csv
import json
import os
from typing import Dict, Any, List

import matplotlib.pyplot as plt


def _load_summary(summary_path: str) -> Dict[str, Any]:
    with open(summary_path, encoding="utf-8") as f:
        return json.load(f)


def _load_customer_report(report_path: str) -> List[Dict[str, Any]]:
    with open(report_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _bar(label: str, value: int, max_value: int, width: int = 40) -> str:
    if max_value <= 0:
        filled = 0
    else:
        filled = int((value / max_value) * width)
    return f"{label:20} | " + "#" * filled + f" ({value})"


def show_loyalty_distribution(summary: Dict[str, Any]) -> None:
    print("\n=== Loyalty Segment Distribution ===")
    segments = [
        ("PLATINUM", summary.get("platinum_customers", 0)),
        ("GOLD", summary.get("gold_customers", 0)),
        ("SILVER", summary.get("silver_customers", 0)),
        ("BRONZE", summary.get("bronze_customers", 0)),
    ]
    max_val = max((v for _, v in segments), default=0)
    for name, val in segments:
        print(_bar(name, val, max_val))


def show_activity_distribution(summary: Dict[str, Any]) -> None:
    print("\n=== Customer Activity Status ===")
    active = summary.get("active_customers", 0)
    inactive = summary.get("inactive_customers", 0)
    max_val = max(active, inactive)
    print(_bar("ACTIVE_CUSTOMER", active, max_val))
    print(_bar("INACTIVE_CUSTOMER", inactive, max_val))


def show_top_customers(report_rows: List[Dict[str, Any]], top_n: int = 5) -> None:
    print(f"\n=== Top {top_n} Customers by Total Spent ===")
    sorted_rows = sorted(
        report_rows,
        key=lambda r: float(r.get("total_spent", 0)),
        reverse=True,
    )
    top_rows = sorted_rows[:top_n]
    print(f"{'Customer ID':12} {'Name':20} {'Orders':>8} {'Total Spent':>15} {'Segment':>10}")
    print("-" * 70)
    for row in top_rows:
        print(
            f"{row.get('customer_id',''):12} "
            f"{row.get('customer_name','')[:20]:20} "
            f"{row.get('total_orders',''):>8} "
            f"{row.get('total_spent',''):>15} "
            f"{row.get('loyalty_segment',''):>10}"
        )


def visualize_outputs_console(
    summary_path: str,
    report_path: str,
) -> None:
    """
    Read the generated analytics outputs and display
    simple text-based charts and tables in the console.
    This does NOT modify any processing logic.
    """
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Summary file not found: {summary_path}")
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Customer report file not found: {report_path}")

    summary = _load_summary(summary_path)
    report_rows = _load_customer_report(report_path)

    print("=== Customer Analytics Visualization ===")
    print(f"Total customers: {summary.get('total_customers', 0)}")
    print(f"Total revenue : {summary.get('total_revenue', 0)}")

    show_loyalty_distribution(summary)
    show_activity_distribution(summary)
    show_top_customers(report_rows, top_n=5)


def visualize_outputs_charts(
    summary_path: str,
    report_path: str,
) -> None:
    """
    Visualize results using matplotlib bar and pie charts.
    This function is optional and does not affect core processing.
    """
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Summary file not found: {summary_path}")
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Customer report file not found: {report_path}")

    summary = _load_summary(summary_path)

    # Loyalty segments bar + pie
    segments = ["PLATINUM", "GOLD", "SILVER", "BRONZE"]
    counts = [
        summary.get("platinum_customers", 0),
        summary.get("gold_customers", 0),
        summary.get("silver_customers", 0),
        summary.get("bronze_customers", 0),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Bar chart
    axes[0].bar(segments, counts, color=["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"])
    axes[0].set_title("Loyalty Segment Distribution")
    axes[0].set_ylabel("Number of Customers")

    # Pie chart
    if sum(counts) > 0:
        axes[1].pie(
            counts,
            labels=segments,
            autopct="%1.1f%%",
            colors=["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"],
        )
        axes[1].set_title("Loyalty Segments Share")
    else:
        axes[1].text(0.5, 0.5, "No data", ha="center", va="center")
        axes[1].set_title("Loyalty Segments Share")

    plt.tight_layout()
    plt.show()

    # Activity status bar chart
    active = summary.get("active_customers", 0)
    inactive = summary.get("inactive_customers", 0)
    labels = ["ACTIVE_CUSTOMER", "INACTIVE_CUSTOMER"]
    values = [active, inactive]

    plt.figure(figsize=(5, 4))
    plt.bar(labels, values, color=["#4daf4a", "#e41a1c"])
    plt.title("Customer Activity Status")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Assume default paths when run directly from the project root.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    summary_file = os.path.join(base_dir, "analytics_summary.json")
    report_file = os.path.join(base_dir, "customer_loyalty_report.csv")

    # Console visualization
    visualize_outputs_console(summary_file, report_file)

    # Graphical visualization (bar and pie charts)
    visualize_outputs_charts(summary_file, report_file)

