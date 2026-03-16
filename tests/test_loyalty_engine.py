from src.loyalty_engine import (
    classify_loyalty_segment,
    determine_activity_status,
)


def test_platinum_customer_classification():
    assert classify_loyalty_segment(10000) == "PLATINUM"
    assert classify_loyalty_segment(15000) == "PLATINUM"


def test_gold_customer_classification():
    assert classify_loyalty_segment(5000) == "GOLD"
    assert classify_loyalty_segment(9999.99) == "GOLD"


def test_silver_customer_classification():
    assert classify_loyalty_segment(1000) == "SILVER"
    assert classify_loyalty_segment(4999.99) == "SILVER"


def test_bronze_customer_classification():
    assert classify_loyalty_segment(0) == "BRONZE"
    assert classify_loyalty_segment(999.99) == "BRONZE"


def test_active_customer_with_orders():
    status = determine_activity_status("ACTIVE", total_orders=3)
    assert status == "ACTIVE_CUSTOMER"


def test_active_customer_without_orders():
    status = determine_activity_status("ACTIVE", total_orders=0)
    assert status == "INACTIVE_CUSTOMER"


def test_inactive_customer_status():
    status = determine_activity_status("INACTIVE", total_orders=5)
    assert status == "INACTIVE_CUSTOMER"

