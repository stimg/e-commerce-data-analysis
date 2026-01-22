# E-Commerce Data Analysis - Refactored Framework

## Overview

This project provides a comprehensive exploratory data analysis (EDA) framework for e-commerce data. The refactored structure separates concerns into modular, reusable components that can be easily configured and extended for different analysis periods and use cases.

## Project Structure

```
e-commerce-data-analysis/
├── EDA_Refactored.ipynb          # Main analysis notebook (configurable)
├── data_loader.py                # Data loading and preparation functions
├── business_metrics.py            # Business metric calculation functions
├── requirements.txt               # Python package dependencies
├── ecommerce_data/               # Data directory
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   └── order_reviews_dataset.csv
└── REFACTORING_README.md         # This file
```

## Key Improvements

### 1. Modular Architecture
The analysis is now split into clean, focused modules:
- **data_loader.py**: Handles all data loading and preparation logic
- **business_metrics.py**: Contains reusable metric calculation functions
- **EDA_Refactored.ipynb**: Clean, well-organized analysis notebook

### 2. Configurable Analysis
The notebook now supports configurable date ranges for analysis:
```python
ANALYSIS_START_YEAR = 2022
ANALYSIS_START_MONTH = None
ANALYSIS_END_YEAR = 2023
ANALYSIS_END_MONTH = None
```
This allows you to analyze any time period without code changes.

### 3. Improved Documentation
- Clear markdown sections with headers
- Data dictionary explaining all columns
- Docstrings for all functions
- Table of contents for easy navigation
- Insights and recommendations section

### 4. Code Quality
- Eliminated SettingWithCopyWarning issues
- Proper error handling with sensible defaults
- Consistent naming conventions
- Type hints for better code clarity
- DRY (Don't Repeat Yourself) principle applied

### 5. Enhanced Visualizations
All charts now include:
- Descriptive titles with date ranges
- Proper axis labels with units
- Consistent color schemes
- Professional formatting
- Grid lines for easier reading

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Ensure the data files are present in the `ecommerce_data/` directory

## Usage

### Running the Analysis

1. Open `EDA_Refactored.ipynb` in Jupyter Notebook or JupyterLab:
```bash
jupyter notebook EDA_Refactored.ipynb
```

2. Configure the analysis parameters in the first code cell:
```python
ANALYSIS_START_YEAR = 2022
ANALYSIS_END_YEAR = 2023
COMPARISON_YEAR = 2022
CURRENT_YEAR = 2023
```

3. Run all cells to generate the complete analysis

### Using the Modules in Python Scripts

You can import and use the modules in your own Python scripts:

```python
from data_loader import load_datasets, prepare_analysis_dataset
from business_metrics import (
    calculate_total_revenue,
    calculate_average_order_value,
    calculate_revenue_by_category
)

# Load data
orders, order_items, products, customers, reviews = load_datasets('ecommerce_data')

# Prepare analysis dataset for specific period
sales_data, products, customers, reviews = prepare_analysis_dataset(
    orders, order_items, products, customers, reviews,
    start_year=2023, end_year=2023
)

# Calculate metrics
revenue = calculate_total_revenue(sales_data)
aov = calculate_average_order_value(sales_data)
revenue_by_state = calculate_revenue_by_state(sales_data, customers)
```

## Module Reference

### data_loader.py

**load_datasets(data_dir='ecommerce_data')**
- Loads all CSV files from the data directory
- Returns: (orders, order_items, products, customers, reviews) DataFrames

**prepare_sales_data(order_items, orders)**
- Merges order items and orders datasets
- Returns: Combined sales DataFrame

**extract_temporal_features(sales_data)**
- Adds 'year' and 'month' columns from timestamps
- Returns: Enhanced DataFrame with temporal features

**filter_delivered_orders(sales_data)**
- Filters to include only delivered orders
- Returns: Filtered DataFrame

**filter_by_date_range(sales_data, start_year, start_month, end_year, end_month)**
- Filters data to specified date range
- Returns: Date-filtered DataFrame

**add_delivery_metrics(sales_data)**
- Calculates delivery speed in days
- Returns: DataFrame with 'delivery_speed' column

**prepare_analysis_dataset(...)**
- Complete preparation pipeline combining all steps
- Returns: Prepared datasets ready for analysis

### business_metrics.py

**Revenue Metrics:**
- `calculate_total_revenue()` - Total sales amount
- `calculate_revenue_by_period()` - Revenue grouped by year/month
- `calculate_revenue_growth()` - YoY or period growth rates
- `calculate_monthly_growth_trend()` - Month-over-month changes

**Order Metrics:**
- `calculate_total_orders()` - Count of unique orders
- `calculate_orders_by_period()` - Order counts by period
- `calculate_average_order_value()` - Mean order value
- `calculate_average_order_value_by_period()` - AOV by period

**Product Analysis:**
- `calculate_revenue_by_category()` - Revenue by product category
- `get_top_categories()` - Top N categories by revenue

**Geographic Analysis:**
- `calculate_revenue_by_state(sales_data, customers)` - Revenue by customer state (requires sales_data with customer_id column)

**Customer Experience:**
- `calculate_delivery_speed_rating_correlation()` - Review scores by delivery days
- `calculate_delivery_time_rating_correlation()` - Review scores by delivery time category
- `calculate_average_review_score()` - Overall satisfaction score
- `calculate_average_delivery_speed()` - Mean delivery time
- `calculate_review_score_distribution()` - Distribution of ratings

**Order Status:**
- `calculate_order_status_distribution()` - Status breakdown by year

**Summary:**
- `calculate_key_metrics()` - Dashboard of all key metrics

## Data Dictionary

### orders_dataset.csv
| Column | Description |
|--------|-------------|
| order_id | Unique order identifier |
| customer_id | Customer reference |
| order_status | Status: canceled, delivered, pending, processing, shipped, returned |
| order_purchase_timestamp | When order was placed |
| order_delivered_customer_date | When order was delivered |

### order_items_dataset.csv
| Column | Description |
|--------|-------------|
| order_id | Order reference |
| order_item_id | Line item number in order |
| product_id | Product reference |
| price | Item price |
| freight_value | Shipping cost |

### products_dataset.csv
| Column | Description |
|--------|-------------|
| product_id | Unique product identifier |
| product_category_name | Product category |
| product_name_length | Length of product name |
| product_description_length | Length of description |
| product_weight_g | Weight in grams |

### customers_dataset.csv
| Column | Description |
|--------|-------------|
| customer_id | Unique customer identifier |
| customer_state | US state of customer |
| customer_city | City of customer |

### order_reviews_dataset.csv
| Column | Description |
|--------|-------------|
| review_id | Unique review identifier |
| order_id | Order reference |
| review_score | Rating from 1 to 5 |
| review_creation_date | When review was posted |

## Customizing the Analysis

### Changing the Analysis Period

Edit the configuration section in the notebook:
```python
ANALYSIS_START_YEAR = 2023
ANALYSIS_START_MONTH = 1      # January
ANALYSIS_END_YEAR = 2023
ANALYSIS_END_MONTH = 12       # December
```

### Changing Comparison Years
```python
COMPARISON_YEAR = 2022
CURRENT_YEAR = 2023
```

### Modifying Visualizations
All matplotlib plots can be customized:
```python
# Change figure size
FIGURE_SIZE = (14, 7)

# Change color scheme
COLOR_PRIMARY = '#1f77b4'
COLOR_SECONDARY = '#ff7f0e'
```

## Key Metrics Explained

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order items
- **YoY Growth**: Percentage change from previous year
- **Monthly Growth**: Month-over-month percentage changes

### Order Metrics
- **Total Orders**: Count of unique order IDs
- **Average Order Value**: Total revenue divided by total orders
- **Order Growth**: Percentage change in order count

### Customer Satisfaction
- **Average Review Score**: Mean rating (1-5 scale)
- **Delivery Speed**: Days between order and delivery
- **Review Distribution**: Breakdown of each rating level

### Geographic Metrics
- **Revenue by State**: Total sales per US state
- **Customer Distribution**: Number of customers per region

## Extending the Framework

To add new metrics:

1. Create a new function in `business_metrics.py`:
```python
def calculate_custom_metric(sales_data):
    """Calculate custom business metric."""
    return sales_data['price'].sum() / sales_data['order_id'].nunique()
```

2. Add a section in the notebook to use it:
```python
from business_metrics import calculate_custom_metric

custom_result = calculate_custom_metric(sales_current)
print(f"Custom Metric: {custom_result}")
```

## Troubleshooting

**Issue**: "No module named 'data_loader'"
- Solution: Ensure you're running the notebook from the project root directory

**Issue**: Data files not found
- Solution: Verify `ecommerce_data/` directory contains all CSV files

**Issue**: MemoryError with large datasets
- Solution: Filter data to smaller date ranges or use data sampling

## Performance Considerations

- The current dataset (15,095 delivered orders) loads and processes in seconds
- Visualization generation adds minimal overhead
- For larger datasets (>1M rows), consider:
  - Filtering to specific date ranges
  - Using data aggregation at the source
  - Implementing incremental processing

## Future Enhancements

Potential improvements for the framework:
- Add caching mechanism for frequently calculated metrics
- Implement automatic report generation
- Add anomaly detection for metrics
- Create interactive dashboards with Plotly
- Add statistical testing and hypothesis validation
- Implement data quality checks and validation
- Add cohort analysis capabilities

## Support

For issues or questions:
1. Check the docstrings in each module
2. Review the analysis sections in EDA_Refactored.ipynb
3. Examine the Data Dictionary section
4. Test individual functions in isolation

## License and Attribution

This refactored analysis framework maintains all original data analysis content while improving code structure, documentation, and reusability.
