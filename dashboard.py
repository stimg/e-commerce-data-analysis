import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from data_loader import load_datasets, prepare_analysis_dataset
from business_metrics import (
    calculate_total_revenue,
    calculate_revenue_growth,
    calculate_revenue_by_period,
    calculate_total_orders,
    calculate_orders_by_period,
    calculate_average_order_value,
    calculate_average_order_value_by_period,
    calculate_revenue_by_category,
    calculate_revenue_by_state,
    calculate_delivery_time_rating_correlation,
    calculate_average_review_score,
    calculate_average_delivery_speed,
    calculate_key_metrics
)

# Page configuration
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Remove Streamlit default styling
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 10px;
        }
        .trend-positive {
            color: #2ca02c;
        }
        .trend-negative {
            color: #d62728;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all datasets"""
    return load_datasets('ecommerce_data')

@st.cache_data
def prepare_data(start_date, end_date):
    """Prepare analysis dataset with date filtering"""
    orders, order_items, products, customers, reviews = load_data()

    # Get start and end year/month from dates
    start_year, start_month = start_date.year, start_date.month
    end_year, end_month = end_date.year, end_date.month

    sales_delivered, products_clean, customers_clean, reviews_clean = prepare_analysis_dataset(
        orders, order_items, products, customers, reviews,
        start_year=start_year, start_month=start_month,
        end_year=end_year, end_month=end_month
    )

    return sales_delivered, products_clean, customers_clean, reviews_clean, orders

def format_currency(value):
    """Format value as currency (e.g., $300K, $2M)"""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.0f}K"
    else:
        return f"${value:.0f}"

def format_currency_axis(value):
    """Format axis labels as currency"""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.0f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.0f}K"
    else:
        return f"${value:.0f}"

def get_trend_indicator(current, previous):
    """Get trend indicator with color and percentage"""
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return "0.00%", "neutral"

    change = ((current - previous) / previous)
    color = "positive" if change >= 0 else "negative"
    return f"{abs(change) * 100:.2f}%", color

def render_kpi_card(col, label, value, trend_pct, trend_color):
    """Render a KPI card"""
    with col:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 14px; color: #666; margin-bottom: 8px;">{label}</div>
                <div style="font-size: 28px; font-weight: bold; margin-bottom: 8px;">{value}</div>
                <div class="trend-{trend_color}" style="font-size: 14px;">
                    {'↑' if trend_color == 'positive' else '↓'} {trend_pct}
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header with date range filter
col1, col2 = st.columns([3, 1])

with col1:
    st.title("E-Commerce Analytics Dashboard")

with col2:
    st.markdown("**Date Range Filter**")

# Date range selection
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime(2022, 1, 1), key="start_date")
with col2:
    end_date = st.date_input("End Date", value=datetime(2023, 12, 31), key="end_date")

# Load and prepare data
sales_delivered, products_clean, customers_clean, reviews_clean, orders = prepare_data(start_date, end_date)

# Calculate comparison period
current_year = end_date.year
previous_year = end_date.year - 1 if end_date.year > start_date.year else start_date.year

sales_current = sales_delivered[sales_delivered['year'] == current_year]
sales_previous = sales_delivered[sales_delivered['year'] == previous_year]

# ============================================================================
# KPI ROW
# ============================================================================

st.markdown("---")

# Calculate KPIs
total_revenue_current = calculate_total_revenue(sales_current)
total_revenue_previous = calculate_total_revenue(sales_previous) if len(sales_previous) > 0 else 0

total_orders_current = calculate_total_orders(sales_current)
total_orders_previous = calculate_total_orders(sales_previous) if len(sales_previous) > 0 else 0

aov_current = calculate_average_order_value(sales_current)
aov_previous = calculate_average_order_value(sales_previous) if len(sales_previous) > 0 else 0

monthly_growth_current = calculate_revenue_growth(total_revenue_current, total_revenue_previous)

# Render KPI cards
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

revenue_trend, revenue_color = get_trend_indicator(total_revenue_current, total_revenue_previous)
render_kpi_card(kpi_col1, "Total Revenue", format_currency(total_revenue_current), revenue_trend, revenue_color)

growth_pct = f"{monthly_growth_current * 100:.2f}%"
growth_color = "positive" if monthly_growth_current >= 0 else "negative"
render_kpi_card(kpi_col2, "Monthly Growth", growth_pct, "—", growth_color)

aov_trend, aov_color = get_trend_indicator(aov_current, aov_previous)
render_kpi_card(kpi_col3, "Average Order Value", format_currency(aov_current), aov_trend, aov_color)

orders_trend, orders_color = get_trend_indicator(total_orders_current, total_orders_previous)
render_kpi_card(kpi_col4, "Total Orders", f"{total_orders_current:,}", orders_trend, orders_color)

# ============================================================================
# CHARTS GRID (2x2)
# ============================================================================

st.markdown("---")

chart_col1, chart_col2 = st.columns(2)

# Chart 1: Revenue Trend Line Chart
with chart_col1:
    monthly_revenue_current = sales_current.groupby('month')['price'].sum().reset_index()
    monthly_revenue_current.columns = ['month', 'revenue']

    # Get previous year data if available
    monthly_revenue_previous = None
    if len(sales_previous) > 0:
        monthly_revenue_previous = sales_previous.groupby('month')['price'].sum().reset_index()
        monthly_revenue_previous.columns = ['month', 'revenue']

    fig_revenue = go.Figure()

    # Add current year line
    fig_revenue.add_trace(go.Scatter(
        x=monthly_revenue_current['month'],
        y=monthly_revenue_current['revenue'],
        mode='lines',
        name=f'Current Year ({current_year})',
        line=dict(color='#1f77b4', width=2, dash='solid'),
        hovertemplate='<b>Month %{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    ))

    # Add previous year line if available
    if monthly_revenue_previous is not None:
        fig_revenue.add_trace(go.Scatter(
            x=monthly_revenue_previous['month'],
            y=monthly_revenue_previous['revenue'],
            mode='lines',
            name=f'Previous Year ({previous_year})',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            hovertemplate='<b>Month %{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        ))

    fig_revenue.update_layout(
        title=f"Revenue Trend - {current_year}",
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode='x unified',
        height=400,
        plot_bgcolor='white',
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            tickformat='$,.0f'
        ),
        xaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_revenue, use_container_width=True)

# Chart 2: Top 10 Categories Bar Chart
with chart_col2:
    category_revenue = calculate_revenue_by_category(sales_current, products_clean)
    top_categories = category_revenue.head(10).sort_values(ascending=True)

    fig_categories = go.Figure(data=[
        go.Bar(
            y=top_categories.index,
            x=top_categories.values,
            orientation='h',
            marker=dict(
                color=top_categories.values,
                colorscale='Blues',
                showscale=False
            ),
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
        )
    ])

    fig_categories.update_layout(
        title="Top 10 Product Categories",
        xaxis_title="Revenue",
        yaxis_title="",
        height=400,
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            tickformat='$,.0f'
        ),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_categories, use_container_width=True)

# Chart 3: Revenue by State (Choropleth)
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    revenue_by_state = calculate_revenue_by_state(sales_current, customers_clean)

    fig_choropleth = px.choropleth(
        revenue_by_state,
        locations='customer_state',
        color='price',
        locationmode='USA-states',
        scope='usa',
        color_continuous_scale='Blues',
        labels={'price': 'Revenue (USD)'},
    )

    fig_choropleth.update_layout(
        title="Revenue by State",
        height=400,
        geo=dict(
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(243, 243, 243)'
        ),
        coloraxis_colorbar=dict(
            title="Revenue",
            tickformat='$,.0f'
        )
    )

    st.plotly_chart(fig_choropleth, use_container_width=True)

# Chart 4: Satisfaction vs Delivery Time
with chart_col4:
    delivery_rating = calculate_delivery_time_rating_correlation(sales_current, reviews_clean)

    fig_delivery = go.Figure(data=[
        go.Bar(
            x=delivery_rating['delivery_time'],
            y=delivery_rating['review_score'],
            marker_color='#1f77b4',
            hovertemplate='<b>%{x}</b><br>Avg Review Score: %{y:.2f}<extra></extra>'
        )
    ])

    fig_delivery.update_layout(
        title="Satisfaction vs Delivery Time",
        xaxis_title="Delivery Time Bucket",
        yaxis_title="Average Review Score",
        height=400,
        plot_bgcolor='white',
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            range=[3.5, 4.5]
        ),
        xaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_delivery, use_container_width=True)

# ============================================================================
# BOTTOM ROW
# ============================================================================

st.markdown("---")

bottom_col1, bottom_col2 = st.columns(2)

# Card 1: Average Delivery Time
with bottom_col1:
    avg_delivery_speed = calculate_average_delivery_speed(sales_current)
    avg_delivery_speed_previous = calculate_average_delivery_speed(sales_previous) if len(sales_previous) > 0 else avg_delivery_speed

    delivery_trend, delivery_color = get_trend_indicator(avg_delivery_speed_previous - avg_delivery_speed, avg_delivery_speed_previous - avg_delivery_speed)

    # Faster delivery is better (negative trend is good)
    if len(sales_previous) > 0 and avg_delivery_speed_previous != 0:
        change = avg_delivery_speed_previous - avg_delivery_speed
        if change > 0:
            delivery_trend = f"{abs(change):.2f} days"
            delivery_color = "positive"
        elif change < 0:
            delivery_trend = f"{abs(change):.2f} days"
            delivery_color = "negative"
        else:
            delivery_trend = "0.00 days"
            delivery_color = "neutral"

    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">Average Delivery Time</div>
            <div style="font-size: 32px; font-weight: bold; margin-bottom: 8px;">{avg_delivery_speed:.1f} days</div>
            <div class="trend-{delivery_color}" style="font-size: 14px;">
                {'↓' if delivery_color == 'positive' else '↑'} {delivery_trend}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Card 2: Review Score
with bottom_col2:
    avg_review_score = calculate_average_review_score(sales_current, reviews_clean)

    # Create star rating display
    stars_full = int(avg_review_score)
    has_half = (avg_review_score % 1) >= 0.5

    star_display = "★" * stars_full + ("✓" if has_half else "")

    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">Average Review Score</div>
            <div style="font-size: 28px; font-weight: bold; margin-bottom: 4px;">{avg_review_score:.2f} / 5.0</div>
            <div style="font-size: 20px; color: #ffc107; margin-bottom: 8px;">{star_display}</div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(f"Dashboard updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
