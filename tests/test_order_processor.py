import pytest

from src.order_processor import (
    filter_valid_orders,
    aggregate_orders_by_customer,
    process_orders_for_customers,
    CustomerOrderMetrics,
)


def _make_customers():
    return [
        {"customer_id": "C1", "customer_name": "Alice", "status": "ACTIVE"},
        {"customer_id": "C2", "customer_name": "Bob", "status": "INACTIVE"},
    ]


def test_customer_order_aggregation():
    customers = _make_customers()
    orders = [
        {
            "order_id": "O1",
            "customer_id": "C1",
            "order_date": "2024-05-05",
            "order_amount": "200",
            "order_status": "DELIVERED",
        },
        {
            "order_id": "O2",
            "customer_id": "C1",
            "order_date": "2024-05-10",
            "order_amount": "300",
            "order_status": "DELIVERED",
        },
        {
            "order_id": "O3",
            "customer_id": "C1",
            "order_date": "2024-05-15",
            "order_amount": "150",
            "order_status": "CANCELLED",
        },
    ]

    metrics = process_orders_for_customers(customers, orders)
    c1_metrics = metrics["C1"]
    assert isinstance(c1_metrics, CustomerOrderMetrics)
    assert c1_metrics.total_orders == 2
    assert c1_metrics.total_spent == 500.0
    assert c1_metrics.average_order_value == 250.0


def test_invalid_order_date_ignored():
    customers = _make_customers()
    orders = [
        {
            "order_id": "O1",
            "customer_id": "C1",
            "order_date": "INVALID_DATE",
            "order_amount": "100",
            "order_status": "DELIVERED",
        }
    ]

    valid = filter_valid_orders(orders)
    assert len(valid) == 0


def test_negative_order_amount_ignored():
    customers = _make_customers()
    orders = [
        {
            "order_id": "O1",
            "customer_id": "C1",
            "order_date": "2024-05-05",
            "order_amount": "-50",
            "order_status": "DELIVERED",
        }
    ]

    valid = filter_valid_orders(orders)
    assert len(valid) == 0

