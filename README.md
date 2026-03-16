## Customer Order Analytics & Loyalty Classification Engine

This project implements a Python-based analytics engine for an e-commerce company to analyze customer purchasing behavior, compute order metrics, and classify customers into loyalty segments.

### Project Structure

- **customers.csv**, **orders.csv**: Input data files at the project root
- **src/**
  - `loader.py`: CSV loading and safe date parsing
  - `order_processor.py`: Order filtering and per-customer aggregation
  - `loyalty_engine.py`: Loyalty segment and activity status classification
  - `reporter.py`: CSV and JSON report generation
  - `main.py`: End-to-end pipeline orchestration and logging setup
- **tests/**
  - `test_order_processor.py`: Aggregation & filtering tests
  - `test_loyalty_engine.py`: Loyalty & activity classification tests
- **logs/**
  - `analytics.log`: Runtime logs (created automatically)

### Requirements

- Python 3.11 (or compatible 3.10+)
- `pytest` (for running unit tests)
- `matplotlib` (for graphical visualizations)

Install pytest (if needed):

```bash
pip install pytest
```

Install matplotlib (if needed):

```bash
pip install matplotlib
```

### Running the Analytics Pipeline

From the project root:

```bash
python -m src.main
```

This will:

- Load `customers.csv` and `orders.csv`
- Filter orders to valid May 2024, non-negative DELIVERED records
- Aggregate per-customer metrics:
  - `total_orders`
  - `total_spent`
  - `average_order_value`
- Classify:
  - `loyalty_segment` (PLATINUM / GOLD / SILVER / BRONZE)
  - `customer_activity_status` (ACTIVE_CUSTOMER / INACTIVE_CUSTOMER)
- Generate:
  - `customer_loyalty_report.csv`
  - `analytics_summary.json`
- Write logs to `logs/analytics.log`

### Running Tests

From the project root:

```bash
pytest
```

The test suite covers:

- Order aggregation and filtering rules
- Loyalty classification thresholds
- Customer activity status rules

### Visualizing the Results (Console View)

After you have run the pipeline and generated `customer_loyalty_report.csv` and `analytics_summary.json`, you can view a simple text-based visualization (ASCII charts and tables) from the project root:

```bash
python -m src.visualizer
```

This will display:

- A bar-chart-style view of loyalty segment counts
- A bar-chart-style view of active vs inactive customers
- A table of the top 5 customers by total spending

### Visualizing the Results as Charts (Bar & Pie)

After running the pipeline and generating `customer_loyalty_report.csv` and `analytics_summary.json`, you can open bar and pie charts using matplotlib:

```bash
python -m src.visualizer
```

This will:

- Show loyalty segment distribution as both a **bar chart** and a **pie chart**
- Show customer activity status as a **bar chart**
