import logging
import os
from typing import List, Dict, Any

from .loader import load_customers, load_orders
from .order_processor import process_orders_for_customers
from .loyalty_engine import enrich_customer_record
from .reporter import (
    write_customer_loyalty_report,
    generate_analytics_summary,
    write_analytics_summary,
)


def setup_logging(log_dir: str) -> None:
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "analytics.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def run_pipeline(
    customers_path: str,
    orders_path: str,
    output_csv_path: str,
    output_json_path: str,
    log_dir: str,
) -> None:
    setup_logging(log_dir)
    logger = logging.getLogger(__name__)

    logger.info("Loading customers from %s", customers_path)
    customers = load_customers(customers_path)
    logger.info("Loading orders from %s", orders_path)
    orders = load_orders(orders_path)

    logger.info("Processing orders for customers")
    metrics_by_customer = process_orders_for_customers(customers, orders)

    # Build enriched records
    enriched_customers: List[Dict[str, Any]] = []
    customer_lookup = {c["customer_id"]: c for c in customers}
    for customer_id, customer in customer_lookup.items():
        metrics = metrics_by_customer.get(customer_id)
        if metrics is None:
            total_orders = 0
            total_spent = 0.0
            avg_value = 0.0
        else:
            total_orders = metrics.total_orders
            total_spent = metrics.total_spent
            avg_value = metrics.average_order_value

        enriched = enrich_customer_record(
            customer,
            total_orders=total_orders,
            total_spent=total_spent,
            average_order_value=avg_value,
        )
        enriched_customers.append(enriched)

    logger.info("Writing customer loyalty report to %s", output_csv_path)
    write_customer_loyalty_report(output_csv_path, enriched_customers)

    logger.info("Generating analytics summary")
    summary = generate_analytics_summary(enriched_customers)
    logger.info("Writing analytics summary to %s", output_json_path)
    write_analytics_summary(output_json_path, summary)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = base_dir
    customers_file = os.path.join(data_dir, "customers.csv")
    orders_file = os.path.join(data_dir, "orders.csv")
    output_csv = os.path.join(base_dir, "customer_loyalty_report.csv")
    output_json = os.path.join(base_dir, "analytics_summary.json")
    logs_dir = os.path.join(base_dir, "logs")

    run_pipeline(
        customers_path=customers_file,
        orders_path=orders_file,
        output_csv_path=output_csv,
        output_json_path=output_json,
        log_dir=logs_dir,
    )

