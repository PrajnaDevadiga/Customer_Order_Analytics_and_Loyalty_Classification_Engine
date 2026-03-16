import csv
from datetime import datetime
from typing import List, Dict, Any, Tuple


def load_customers(file_path: str) -> List[Dict[str, Any]]:
    """Load customers from CSV into a list of dicts."""
    customers: List[Dict[str, Any]] = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)
    return customers


def load_orders(file_path: str) -> List[Dict[str, Any]]:
    """Load orders from CSV into a list of dicts."""
    orders: List[Dict[str, Any]] = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders.append(row)
    return orders


def parse_date_safe(date_str: str) -> Tuple[bool, Any]:
    """
    Safely parse a date string in ISO format (YYYY-MM-DD).
    Returns (True, datetime) on success, (False, None) on failure.
    """
    try:
        return True, datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return False, None

