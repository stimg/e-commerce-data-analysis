# E-Commerce Data Analysis

A comprehensive analysis and interactive dashboard for e-commerce data, featuring both Jupyter notebook exploration and a professional Streamlit dashboard.

## Overview

This project provides tools for analyzing e-commerce performance metrics including revenue trends, customer behavior, product performance, and geographic distribution of sales. The analysis examines data from 2022-2023 with the ability to filter by custom date ranges.

## Contents

- **EDA_Refactored.ipynb** - Comprehensive Jupyter notebook with exploratory data analysis
- **dashboard.py** - Interactive Streamlit dashboard with real-time filtering
- **data_loader.py** - Utility functions for loading and preparing datasets
- **business_metrics.py** - Functions for calculating key business metrics
- **ecommerce_data/** - Raw CSV datasets directory

## Features

### Dashboard Highlights

The Streamlit dashboard provides a professional, interactive interface with:

#### Header Section
- Application title
- Global date range filter (applies to all visualizations)

#### KPI Row (4 Cards)
- **Total Revenue** - Total sales with year-over-year growth trend
- **Monthly Growth** - Month-over-month revenue change percentage
- **Average Order Value (AOV)** - Mean transaction value with trend indicator
- **Total Orders** - Order volume with trend comparison

Each KPI card displays:
- Large, readable metric value
- Trend indicator (↑ for growth, ↓ for decline)
- Percentage change with color coding (green for positive, red for negative)

#### Analytics Charts (2x2 Grid)

1. **Revenue Trend Line Chart**
   - Solid line for current period
   - Dashed line for previous period (comparison)
   - Grid lines for easier reading
   - Y-axis formatted as $300K, $2M, etc.

2. **Top 10 Categories Bar Chart**
   - Horizontal bar chart sorted in descending order
   - Blue gradient coloring based on revenue amount
   - Values formatted as $300K, $2M

3. **Revenue by State (US Choropleth Map)**
   - Color-coded by revenue amount
   - Blue gradient color scale
   - Interactive hover details
   - Albers USA projection for accurate representation

4. **Customer Satisfaction vs Delivery Time**
   - Bar chart showing average review scores
   - Delivery time buckets (1-3 days, 4-7 days, etc.)
   - Demonstrates correlation between faster delivery and higher satisfaction

#### Bottom Row (2 Cards)

1. **Average Delivery Time**
   - Large display of average days to delivery
   - Trend indicator showing improvement/decline vs previous period
   - Color-coded trend arrow

2. **Review Score**
   - Large average review score (out of 5.0)
   - Star rating display
   - Subtitle: "Average Review Score"

## Data Dictionary

### Key Tables

**orders_dataset.csv**
- `order_id` - Unique identifier for each order
- `customer_id` - Identifier linking to the customer
- `order_status` - Current status (canceled, delivered, pending, processing, shipped, returned)
- `order_purchase_timestamp` - Date and time order was placed
- `order_delivered_customer_date` - Date order was delivered

**order_items_dataset.csv**
- `order_id` - Links to orders table
- `product_id` - Links to products table
- `price` - Price of individual item
- `freight_value` - Shipping cost for item

**products_dataset.csv**
- `product_id` - Unique product identifier
- `product_category_name` - Product category
- `product_description_length` - Description length

**customers_dataset.csv**
- `customer_id` - Unique customer identifier
- `customer_state` - State location (US states)
- `customer_city` - City location

**order_reviews_dataset.csv**
- `review_id` - Unique review identifier
- `order_id` - Links to orders table
- `review_score` - Rating from 1-5
- `review_creation_date` - When review was posted

## Installation

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files are in place**
   - Place CSV files in the `ecommerce_data/` directory

## Usage

### Running the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`. Use the date range filter in the header to dynamically update all visualizations.

### Running the Jupyter Notebook

```bash
jupyter notebook EDA_Refactored.ipynb
```

The notebook provides detailed exploratory analysis with configuration parameters at the top for adjusting the analysis period.

## Key Metrics

The dashboard calculates and displays:

- **Total Revenue** - Sum of all order values
- **Revenue Growth** - Year-over-year percentage change
- **Average Order Value (AOV)** - Mean revenue per order
- **Total Orders** - Count of delivered orders
- **Average Delivery Speed** - Days from order to delivery
- **Average Review Score** - Customer satisfaction rating (1-5 scale)
- **Revenue by Category** - Sales distribution across product categories
- **Revenue by State** - Geographic sales distribution
- **Delivery Time vs Satisfaction** - Correlation analysis

## Technical Details

### Technologies Used
- **Streamlit** - Interactive dashboard framework
- **Plotly** - Interactive charting library
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Matplotlib** - Static visualization (EDA notebook)

### Styling
- Professional card-based layout
- Consistent color scheme (blue primary, red/green for trends)
- Responsive design that adapts to different screen sizes
- Custom HTML/CSS for KPI cards
- Plotly's built-in interactivity for charts

## Analysis Insights

Based on 2022-2023 data analysis:

1. **Revenue Performance** - Slight decline of 2.46% year-over-year
2. **Order Volume** - 2.40% decrease in order count
3. **AOV Stability** - Average order value remained stable at ~$725
4. **Customer Satisfaction** - Consistent 4.1/5.0 average review score
5. **Delivery Performance** - Maintained ~8 days average delivery
6. **Geographic Distribution** - Sales across all US states with California leading

## Customization

### Adjusting Date Range
Use the date filters in the dashboard header to analyze any period within your dataset.

### Modifying Chart Colors
Edit the color definitions in `dashboard.py`:
- `COLOR_PRIMARY` - Primary chart color
- Plotly colorscales for gradients

### Adding New Metrics
Use the `calculate_*` functions in `business_metrics.py` to add new KPIs or charts.

## Troubleshooting

**Issue**: Data not loading
- Ensure CSV files are in the `ecommerce_data/` directory
- Check that filenames match exactly in `data_loader.py`

**Issue**: Charts not displaying
- Verify Plotly is installed: `pip install --upgrade plotly`
- Clear Streamlit cache: `streamlit cache clear`

**Issue**: Date filter not affecting charts
- Check that the date range is within your dataset's date boundaries
- Verify data preparation filters in `prepare_data()` function

## Future Enhancements

- Customer segmentation analysis
- Predictive revenue forecasting
- Product performance drill-down
- Customer lifetime value calculations
- Inventory optimization insights
- Marketing attribution analysis

## License

This project is provided as-is for educational and analytical purposes.

## Support

For questions or issues, refer to the inline documentation in:
- `business_metrics.py` - Metric calculation functions
- `data_loader.py` - Data loading and preparation
- `dashboard.py` - Dashboard structure and components
