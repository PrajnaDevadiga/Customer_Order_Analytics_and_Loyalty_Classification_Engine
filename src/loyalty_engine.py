from typing import Dict, Any


def classify_loyalty_segment(total_spent: float) -> str:
    if total_spent >= 10000:
        return "PLATINUM"
    if total_spent >= 5000:
        return "GOLD"
    if total_spent >= 1000:
        return "SILVER"
    return "BRONZE"


def determine_activity_status(customer_status: str, total_orders: int) -> str:
    """
    - ACTIVE with zero orders -> INACTIVE_CUSTOMER
    - INACTIVE remains INACTIVE_CUSTOMER
    - ACTIVE with orders -> ACTIVE_CUSTOMER
    """
    base_status = (customer_status or "").upper()
    if base_status == "INACTIVE":
        return "INACTIVE_CUSTOMER"
    if base_status == "ACTIVE":
        if total_orders > 0:
            return "ACTIVE_CUSTOMER"
        return "INACTIVE_CUSTOMER"
    # Fallback for unexpected statuses
    return "INACTIVE_CUSTOMER"


def enrich_customer_record(
    customer: Dict[str, Any],
    total_orders: int,
    total_spent: float,
    average_order_value: float,
) -> Dict[str, Any]:
    loyalty_segment = classify_loyalty_segment(total_spent)
    activity_status = determine_activity_status(customer.get("status", ""), total_orders)

    return {
        "customer_id": customer.get("customer_id"),
        "customer_name": customer.get("customer_name"),
        "total_orders": total_orders,
        "total_spent": round(total_spent, 2),
        "average_order_value": round(average_order_value, 2),
        "loyalty_segment": loyalty_segment,
        "customer_activity_status": activity_status,
    }

