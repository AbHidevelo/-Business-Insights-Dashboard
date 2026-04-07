import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Sales Dashboard", layout="wide")

engine = create_engine("postgresql+psycopg2://abhi:1234@127.0.0.1:5432/superstore")

@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

# Sidebar
page = st.sidebar.radio("Navigate", ["Overview", "Trends", "Products"])

# ================= OVERVIEW =================
st.title("📊 Business-Insights-Dashboard")
st.caption("End-to-end analytics project using PostgreSQL, SQL, and Streamlit")
if page == "Overview":
    st.title("Business Overview")

    # KPIs
    kpi_query = """
    SELECT 
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit,
        COUNT(order_id) AS total_orders
    FROM orders
    """
    kpi_df = pd.read_sql(kpi_query, engine)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", int(kpi_df["total_sales"][0]))
    col2.metric("Total Profit", int(kpi_df["total_profit"][0]))
    col3.metric("Total Orders", int(kpi_df["total_orders"][0]))

    st.divider()

    # Region Sales
    region_query = """
    SELECT region, SUM(sales) AS total_sales
    FROM orders
    GROUP BY region
    ORDER BY total_sales DESC
    """
    region_df = pd.read_sql(region_query, engine)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Sales by Region")
        st.bar_chart(region_df.set_index("region"))

    # Category Sales
    category_query = """
    SELECT category, SUM(sales) AS total_sales
    FROM orders
    GROUP BY category
    ORDER BY total_sales DESC
    """
    cat_df = pd.read_sql(category_query, engine)

    with col2:
        st.subheader("📦 Sales by Category")
        st.bar_chart(cat_df.set_index("category"))

# ================= TRENDS =================
elif page == "Trends":
    st.title("📈 Sales & Profit Trends")

    trend_query = """
    SELECT 
        DATE_TRUNC('month', order_date) AS month,
        SUM(sales) AS total_sales,
        SUM(profit) AS total_profit,
        COUNT(order_id) AS total_orders
    FROM orders
    GROUP BY month
    ORDER BY month
    """
    df = pd.read_sql(trend_query, engine)

    df = df.set_index("month")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Monthly Sales")
        st.line_chart(df["total_sales"])

    with col2:
        st.subheader("💰 Monthly Profit")
        st.line_chart(df["total_profit"])

    st.subheader("📦 Order Volume Trend")
    st.line_chart(df["total_orders"])

# ================= PRODUCTS =================
elif page == "Products":
    st.title("📦 Product Performance")

    # Top Products
    product_query = """
    SELECT product_name, SUM(sales) AS total_sales
    FROM orders
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 10
    """
    product_df = pd.read_sql(product_query, engine)

    st.subheader("🏆 Top 10 Products")
    st.bar_chart(product_df.set_index("product_name"))

    st.divider()

    # Sub-category
    subcat_query = """
    SELECT sub_category, SUM(sales) AS total_sales, SUM(profit) AS total_profit
    FROM orders
    GROUP BY sub_category
    ORDER BY total_sales DESC
    """
    subcat_df = pd.read_sql(subcat_query, engine)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sub-Category Sales")
        st.bar_chart(subcat_df.set_index("sub_category")["total_sales"])

    with col2:
        st.subheader("💰 Sub-Category Profit")
        st.bar_chart(subcat_df.set_index("sub_category")["total_profit"])