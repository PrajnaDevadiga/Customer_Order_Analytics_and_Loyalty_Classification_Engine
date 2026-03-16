import csv
import json
from typing import Dict, Any, List


def write_customer_loyalty_report(
    output_path: str,
    enriched_customers: List[Dict[str, Any]],
) -> None:
    fieldnames = [
        "customer_id",
        "customer_name",
        "total_orders",
        "total_spent",
        "average_order_value",
        "loyalty_segment",
        "customer_activity_status",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in enriched_customers:
            writer.writerow(row)


def generate_analytics_summary(
    enriched_customers: List[Dict[str, Any]],
) -> Dict[str, Any]:
    total_customers = len(enriched_customers)
    active_customers = sum(
        1 for c in enriched_customers if c["customer_activity_status"] == "ACTIVE_CUSTOMER"
    )
    inactive_customers = sum(
        1 for c in enriched_customers if c["customer_activity_status"] == "INACTIVE_CUSTOMER"
    )
    platinum_customers = sum(1 for c in enriched_customers if c["loyalty_segment"] == "PLATINUM")
    gold_customers = sum(1 for c in enriched_customers if c["loyalty_segment"] == "GOLD")
    silver_customers = sum(1 for c in enriched_customers if c["loyalty_segment"] == "SILVER")
    bronze_customers = sum(1 for c in enriched_customers if c["loyalty_segment"] == "BRONZE")
    total_revenue = round(sum(c["total_spent"] for c in enriched_customers), 2)

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "inactive_customers": inactive_customers,
        "platinum_customers": platinum_customers,
        "gold_customers": gold_customers,
        "silver_customers": silver_customers,
        "bronze_customers": bronze_customers,
        "total_revenue": total_revenue,
    }


def write_analytics_summary(output_path: str, summary: Dict[str, Any]) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

