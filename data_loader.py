"""
Data loader and preparation module for e-commerce analysis.

This module handles loading, cleaning, and preparing data from CSV files
for exploratory data analysis.
"""

import pandas as pd
from datetime import datetime
from typing import Tuple, Optional


def load_datasets(data_dir: str = 'ecommerce_data') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load all datasets from the specified directory.

    Parameters
    ----------
    data_dir : str
        Directory path containing the CSV files. Default is 'ecommerce_data'.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
        Tuple of (orders, order_items, products, customers, reviews) DataFrames.
    """
    orders = pd.read_csv(f'{data_dir}/orders_dataset.csv')
    order_items = pd.read_csv(f'{data_dir}/order_items_dataset.csv')
    products = pd.read_csv(f'{data_dir}/products_dataset.csv')
    customers = pd.read_csv(f'{data_dir}/customers_dataset.csv')
    reviews = pd.read_csv(f'{data_dir}/order_reviews_dataset.csv')

    return orders, order_items, products, customers, reviews


def prepare_sales_data(order_items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    Merge order items and orders data to create a comprehensive sales dataset.

    Parameters
    ----------
    order_items : pd.DataFrame
        Order items dataset containing price and product information.
    orders : pd.DataFrame
        Orders dataset containing order status and timestamp information.

    Returns
    -------
    pd.DataFrame
        Merged dataset with sales information including order status and timestamps.
    """
    sales_data = pd.merge(
        left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
        right=orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date']],
        on='order_id'
    )

    return sales_data


def extract_temporal_features(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract temporal features from sales data.

    Adds year and month columns based on the order_purchase_timestamp.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with order_purchase_timestamp column.

    Returns
    -------
    pd.DataFrame
        Dataset with added 'year' and 'month' columns.
    """
    sales_data = sales_data.copy()
    sales_data['order_purchase_timestamp'] = pd.to_datetime(sales_data['order_purchase_timestamp'])
    sales_data['year'] = sales_data['order_purchase_timestamp'].dt.year
    sales_data['month'] = sales_data['order_purchase_timestamp'].dt.month

    return sales_data


def filter_delivered_orders(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter sales data to include only delivered orders.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with order_status column.

    Returns
    -------
    pd.DataFrame
        Dataset containing only delivered orders.
    """
    return sales_data[sales_data['order_status'] == 'delivered'].copy()


def filter_by_date_range(sales_data: pd.DataFrame,
                         start_year: Optional[int] = None,
                         start_month: Optional[int] = None,
                         end_year: Optional[int] = None,
                         end_month: Optional[int] = None) -> pd.DataFrame:
    """
    Filter sales data by a specified date range.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'year' and 'month' columns.
    start_year : int, optional
        Starting year for filter. If None, includes all years from beginning.
    start_month : int, optional
        Starting month for filter. If None and start_year is provided, starts from January.
    end_year : int, optional
        Ending year for filter. If None, includes all years to end.
    end_month : int, optional
        Ending month for filter. If None and end_year is provided, ends at December.

    Returns
    -------
    pd.DataFrame
        Filtered dataset for the specified date range.
    """
    data = sales_data.copy()

    if start_year is not None:
        start_month = start_month or 1
        data = data[(data['year'] > start_year) |
                    ((data['year'] == start_year) & (data['month'] >= start_month))]

    if end_year is not None:
        end_month = end_month or 12
        data = data[(data['year'] < end_year) |
                    ((data['year'] == end_year) & (data['month'] <= end_month))]

    return data


def add_delivery_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate delivery speed metrics.

    Converts delivery timestamps to datetime and calculates delivery speed in days.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with delivery timestamps.

    Returns
    -------
    pd.DataFrame
        Dataset with added 'delivery_speed' column (in days).
    """
    data = sales_data.copy()
    data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'])
    data['delivery_speed'] = (
        data['order_delivered_customer_date'] - data['order_purchase_timestamp']
    ).dt.days

    return data


def prepare_analysis_dataset(orders: pd.DataFrame,
                             order_items: pd.DataFrame,
                             products: pd.DataFrame,
                             customers: pd.DataFrame,
                             reviews: pd.DataFrame,
                             start_year: Optional[int] = None,
                             start_month: Optional[int] = None,
                             end_year: Optional[int] = None,
                             end_month: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Complete data preparation pipeline for analysis.

    Loads, cleans, and prepares all datasets for analysis within a specified date range.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders dataset.
    order_items : pd.DataFrame
        Order items dataset.
    products : pd.DataFrame
        Products dataset.
    customers : pd.DataFrame
        Customers dataset.
    reviews : pd.DataFrame
        Reviews dataset.
    start_year : int, optional
        Starting year for analysis period.
    start_month : int, optional
        Starting month for analysis period.
    end_year : int, optional
        Ending year for analysis period.
    end_month : int, optional
        Ending month for analysis period.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        Tuple of (sales_delivered, products, customers, reviews) prepared for analysis.
    """
    # Prepare sales data
    sales_data = prepare_sales_data(order_items, orders)
    sales_data = extract_temporal_features(sales_data)
    sales_delivered = filter_delivered_orders(sales_data)
    sales_delivered = filter_by_date_range(
        sales_delivered, start_year, start_month, end_year, end_month
    )
    sales_delivered = add_delivery_metrics(sales_delivered)

    return sales_delivered, products, customers, reviews
