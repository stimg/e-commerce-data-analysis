"""
Business metrics calculation module for e-commerce analysis.

This module provides functions to calculate various business metrics from
order and sales data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


# Revenue Metrics

def calculate_total_revenue(sales_data: pd.DataFrame) -> float:
    """
    Calculate total revenue from sales data.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'price' column.

    Returns
    -------
    float
        Total revenue (sum of all prices).
    """
    return sales_data['price'].sum()


def calculate_revenue_by_period(sales_data: pd.DataFrame,
                                period_column: str = 'year') -> pd.Series:
    """
    Calculate total revenue grouped by a specified period.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'price' column and period column.
    period_column : str
        Column name for grouping (e.g., 'year', 'month'). Default is 'year'.

    Returns
    -------
    pd.Series
        Revenue by period.
    """
    return sales_data.groupby(period_column)['price'].sum()


def calculate_revenue_growth(current_period_revenue: float,
                             previous_period_revenue: float) -> float:
    """
    Calculate percentage revenue growth between two periods.

    Parameters
    ----------
    current_period_revenue : float
        Revenue for the current period.
    previous_period_revenue : float
        Revenue for the previous period.

    Returns
    -------
    float
        Percentage growth (as decimal, e.g., 0.1 = 10%).
    """
    if previous_period_revenue == 0:
        return 0.0
    return (current_period_revenue - previous_period_revenue) / previous_period_revenue


def calculate_monthly_growth_trend(sales_data: pd.DataFrame) -> pd.Series:
    """
    Calculate month-over-month revenue growth rates.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'price' and 'month' columns.

    Returns
    -------
    pd.Series
        Month-over-month percentage changes.
    """
    monthly_revenue = sales_data.groupby('month')['price'].sum()
    return monthly_revenue.pct_change()


# Order Metrics

def calculate_total_orders(sales_data: pd.DataFrame) -> int:
    """
    Calculate the total number of unique orders.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' column.

    Returns
    -------
    int
        Total number of unique orders.
    """
    return sales_data['order_id'].nunique()


def calculate_orders_by_period(sales_data: pd.DataFrame,
                               period_column: str = 'year') -> pd.Series:
    """
    Calculate number of orders grouped by a specified period.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' and period column.
    period_column : str
        Column name for grouping (e.g., 'year', 'month'). Default is 'year'.

    Returns
    -------
    pd.Series
        Number of orders by period.
    """
    return sales_data.groupby(period_column)['order_id'].nunique()


# Average Order Value

def calculate_average_order_value(sales_data: pd.DataFrame) -> float:
    """
    Calculate average order value (total revenue / total orders).

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' and 'price' columns.

    Returns
    -------
    float
        Average value per order.
    """
    order_values = sales_data.groupby('order_id')['price'].sum()
    return order_values.mean()


def calculate_average_order_value_by_period(sales_data: pd.DataFrame,
                                            period_column: str = 'year') -> pd.Series:
    """
    Calculate average order value grouped by a specified period.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id', 'price' and period column.
    period_column : str
        Column name for grouping. Default is 'year'.

    Returns
    -------
    pd.Series
        Average order value by period.
    """
    aov_by_period = []
    for period in sorted(sales_data[period_column].unique()):
        period_data = sales_data[sales_data[period_column] == period]
        aov = calculate_average_order_value(period_data)
        aov_by_period.append(aov)

    return pd.Series(aov_by_period, index=sorted(sales_data[period_column].unique()))


# Product Analysis

def calculate_revenue_by_category(sales_data: pd.DataFrame,
                                  products: pd.DataFrame) -> pd.Series:
    """
    Calculate total revenue by product category.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'product_id' and 'price' columns.
    products : pd.DataFrame
        Products dataset with 'product_id' and 'product_category_name' columns.

    Returns
    -------
    pd.Series
        Revenue by product category, sorted in descending order.
    """
    sales_with_categories = pd.merge(
        left=products[['product_id', 'product_category_name']],
        right=sales_data[['product_id', 'price']],
        on='product_id'
    )

    return sales_with_categories.groupby('product_category_name')['price'].sum().sort_values(ascending=False)


def get_top_categories(sales_data: pd.DataFrame,
                       products: pd.DataFrame,
                       top_n: int = 5) -> pd.Series:
    """
    Get the top N product categories by revenue.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'product_id' and 'price' columns.
    products : pd.DataFrame
        Products dataset.
    top_n : int
        Number of top categories to return. Default is 5.

    Returns
    -------
    pd.Series
        Top N categories by revenue.
    """
    category_revenue = calculate_revenue_by_category(sales_data, products)
    return category_revenue.head(top_n)


# Geographic Analysis

def calculate_revenue_by_state(sales_data: pd.DataFrame,
                               orders: pd.DataFrame,
                               customers: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total revenue by customer state.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' and 'price' columns.
    orders : pd.DataFrame
        Orders dataset with 'order_id' and 'customer_id' columns.
    customers : pd.DataFrame
        Customers dataset with 'customer_id' and 'customer_state' columns.

    Returns
    -------
    pd.DataFrame
        Revenue by state, sorted in descending order.
    """
    sales_with_customers = pd.merge(
        left=sales_data[['order_id', 'price']],
        right=orders[['order_id', 'customer_id']],
        on='order_id'
    )

    sales_with_states = pd.merge(
        left=sales_with_customers,
        right=customers[['customer_id', 'customer_state']],
        on='customer_id'
    )

    revenue_by_state = sales_with_states.groupby('customer_state')['price'].sum().sort_values(ascending=False)

    result = revenue_by_state.reset_index()
    result.columns = ['customer_state', 'price']

    return result


# Customer Experience Metrics

def calculate_delivery_speed_rating_correlation(sales_data: pd.DataFrame,
                                                reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average review score by delivery speed.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' and 'delivery_speed' columns.
    reviews : pd.DataFrame
        Reviews dataset with 'order_id' and 'review_score' columns.

    Returns
    -------
    pd.DataFrame
        Average review score grouped by delivery speed (in days).
    """
    merged = pd.merge(
        left=sales_data[['order_id', 'delivery_speed']],
        right=reviews[['order_id', 'review_score']],
        on='order_id'
    )

    result = merged.groupby('delivery_speed')['review_score'].mean().reset_index()
    result.columns = ['delivery_speed', 'avg_review_score']

    return result


def categorize_delivery_time(days: int) -> str:
    """
    Categorize delivery speed into time buckets.

    Parameters
    ----------
    days : int
        Number of days for delivery.

    Returns
    -------
    str
        Delivery time category ('1-3 days', '4-7 days', or '8+ days').
    """
    if days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def calculate_delivery_time_rating_correlation(sales_data: pd.DataFrame,
                                               reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average review score by delivery time category.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' and 'delivery_speed' columns.
    reviews : pd.DataFrame
        Reviews dataset with 'order_id' and 'review_score' columns.

    Returns
    -------
    pd.DataFrame
        Average review score grouped by delivery time category.
    """
    merged = pd.merge(
        left=sales_data[['order_id', 'delivery_speed']],
        right=reviews[['order_id', 'review_score']],
        on='order_id'
    ).drop_duplicates(subset=['order_id'])

    merged['delivery_time'] = merged['delivery_speed'].apply(categorize_delivery_time)
    result = merged.groupby('delivery_time')['review_score'].mean().reset_index()

    return result


def calculate_average_review_score(sales_data: pd.DataFrame,
                                   reviews: pd.DataFrame) -> float:
    """
    Calculate overall average review score for orders.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' column.
    reviews : pd.DataFrame
        Reviews dataset with 'order_id' and 'review_score' columns.

    Returns
    -------
    float
        Average review score across all reviewed orders.
    """
    merged = pd.merge(
        left=sales_data[['order_id']].drop_duplicates(),
        right=reviews[['order_id', 'review_score']],
        on='order_id',
        how='inner'
    )

    return merged['review_score'].mean()


def calculate_average_delivery_speed(sales_data: pd.DataFrame) -> float:
    """
    Calculate average delivery speed in days.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'delivery_speed' column.

    Returns
    -------
    float
        Average delivery speed in days.
    """
    return sales_data['delivery_speed'].mean()


def calculate_review_score_distribution(sales_data: pd.DataFrame,
                                        reviews: pd.DataFrame) -> pd.Series:
    """
    Calculate distribution of review scores.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with 'order_id' column.
    reviews : pd.DataFrame
        Reviews dataset with 'review_score' column.

    Returns
    -------
    pd.Series
        Normalized count of review scores (proportions).
    """
    merged = pd.merge(
        left=sales_data[['order_id']].drop_duplicates(),
        right=reviews[['order_id', 'review_score']],
        on='order_id',
        how='inner'
    )

    return merged['review_score'].value_counts(normalize=True).sort_index()


# Order Status Analysis

def calculate_order_status_distribution(orders: pd.DataFrame,
                                       year: Optional[int] = None) -> pd.Series:
    """
    Calculate distribution of order statuses.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders dataset with 'order_status' and optionally 'year' columns.
    year : int, optional
        Filter orders to a specific year. If None, includes all years.

    Returns
    -------
    pd.Series
        Normalized count of each order status (proportions).
    """
    data = orders.copy()

    if year is not None:
        if 'year' not in data.columns:
            data['year'] = pd.to_datetime(data['order_purchase_timestamp']).dt.year
        data = data[data['year'] == year]

    return data['order_status'].value_counts(normalize=True).sort_values(ascending=False)


# Summary Metrics

def calculate_key_metrics(sales_data: pd.DataFrame,
                         products: pd.DataFrame,
                         customers: pd.DataFrame,
                         reviews: pd.DataFrame,
                         orders: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate key business metrics for quick overview.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data.
    products : pd.DataFrame
        Products dataset.
    customers : pd.DataFrame
        Customers dataset.
    reviews : pd.DataFrame
        Reviews dataset.
    orders : pd.DataFrame
        Orders dataset.

    Returns
    -------
    Dict[str, float]
        Dictionary of key metrics including revenue, orders, AOV, and ratings.
    """
    return {
        'total_revenue': calculate_total_revenue(sales_data),
        'total_orders': calculate_total_orders(sales_data),
        'average_order_value': calculate_average_order_value(sales_data),
        'average_review_score': calculate_average_review_score(sales_data, reviews),
        'average_delivery_speed_days': calculate_average_delivery_speed(sales_data),
        'unique_customers': sales_data['order_id'].nunique() if 'order_id' in sales_data.columns else 0,
    }
