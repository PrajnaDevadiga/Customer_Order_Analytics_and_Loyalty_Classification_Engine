from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Any, Tuple
import logging

from .loader import parse_date_safe


LOGGER = logging.getLogger(__name__)


MAY_2024_START = date(2024, 5, 1)
MAY_2024_END = date(2024, 5, 31)


@dataclass
class CustomerOrderMetrics:
    customer_id: str
    total_orders: int = 0
    total_spent: float = 0.0

    @property
    def average_order_value(self) -> float:
        if self.total_orders == 0:
            return 0.0
        return self.total_spent / self.total_orders


def _is_order_in_may_2024(order_date_str: str) -> bool:
    ok, dt = parse_date_safe(order_date_str)
    if not ok or dt is None:
        LOGGER.warning("Invalid order date skipped: %s", order_date_str)
        return False
    return MAY_2024_START <= dt <= MAY_2024_END


def filter_valid_orders(
    orders: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Apply filtering rules:
    - Only orders from May 2024
    - Ignore invalid dates
    - Ignore negative amounts
    """
    valid: List[Dict[str, Any]] = []
    for order in orders:
        if not _is_order_in_may_2024(order.get("order_date", "")):
            continue
        try:
            amount = float(order.get("order_amount", "0"))
        except ValueError:
            LOGGER.warning("Non-numeric order amount skipped: %s", order.get("order_amount"))
            continue
        if amount < 0:
            LOGGER.warning("Negative order amount ignored for order_id=%s", order.get("order_id"))
            continue
        valid.append(order)
    return valid


def aggregate_orders_by_customer(
    customers: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
) -> Dict[str, CustomerOrderMetrics]:
    """
    Aggregate order metrics per customer.
    - Only DELIVERED orders contribute to revenue and order counts.
    - CANCELLED and RETURNED do not contribute to revenue.
    - Customers with no valid orders must still appear.
    - Unknown customer IDs in orders are logged and skipped.
    """
    customer_lookup: Dict[str, Dict[str, Any]] = {
        c["customer_id"]: c for c in customers
    }

    metrics: Dict[str, CustomerOrderMetrics] = {
        cid: CustomerOrderMetrics(customer_id=cid) for cid in customer_lookup.keys()
    }

    for order in orders:
        cid = order.get("customer_id")
        if cid not in customer_lookup:
            LOGGER.warning("Order with unknown customer_id encountered: %s", cid)
            continue

        status = order.get("order_status", "").upper()
        try:
            amount = float(order.get("order_amount", "0"))
        except ValueError:
            LOGGER.warning("Non-numeric order amount skipped in aggregation for order_id=%s", order.get("order_id"))
            continue

        if status == "DELIVERED":
            m = metrics[cid]
            m.total_orders += 1
            m.total_spent += amount
        # CANCELLED and RETURNED: explicitly no effect

    return metrics


def process_orders_for_customers(
    customers: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
) -> Dict[str, CustomerOrderMetrics]:
    """
    High-level processing entry:
    1. Filter valid orders.
    2. Aggregate metrics per customer.
    """
    valid_orders = filter_valid_orders(orders)
    return aggregate_orders_by_customer(customers, valid_orders)

