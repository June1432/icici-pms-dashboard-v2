import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="JANE PMS Dashboard", layout="wide")

# Define roles
roles = ["Relationship Manager", "Fund Manager", "Distributor", "Investor"]

# Sidebar for role selection
st.sidebar.title("User Role")
role = st.sidebar.selectbox("Select your role:", roles)

# Dummy data
clients_df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Category": ["HNI", "Retail", "UHNI", "Retail"],
    "City": ["Mumbai", "Delhi", "Bangalore", "Hyderabad"],
    "AUM (Cr)": [3.5, 0.6, 12.0, 0.9],
    "Risk": ["High", "Low", "Medium", "Low"],
})

# RM View
if role == "Relationship Manager":
    st.title("👤 Relationship Manager Dashboard")
    st.subheader("Client Overview")
    
    total_clients = len(clients_df)
    total_aum = clients_df["AUM (Cr)"].sum()
    category_counts = clients_df["Category"].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", total_clients)
    col2.metric("Total AUM (Cr)", f"₹ {total_aum:.2f}")
    col3.metric("Retail Clients", category_counts.get("Retail", 0))

    st.subheader("Client Breakdown")
    st.dataframe(clients_df)

    st.subheader("Demographics")
    st.bar_chart(clients_df["City"].value_counts())

# FM View
elif role == "Fund Manager":
    st.title("📈 Fund Manager Dashboard")
    st.subheader("Portfolio Allocation Overview")

    portfolio_data = pd.DataFrame({
        "Asset Class": ["Equity", "Debt", "Gold", "Cash"],
        "Allocation (%)": [50, 30, 10, 10]
    })

    st.dataframe(portfolio_data)
    st.subheader("Performance vs Benchmark")
    performance = pd.DataFrame({
        "Month": pd.date_range("2024-01-01", periods=6, freq='M'),
        "Fund Return (%)": [2.1, 1.8, 3.0, -0.5, 2.4, 1.1],
        "Benchmark Return (%)": [1.9, 2.0, 2.5, -0.2, 1.8, 1.3]
    })
    st.line_chart(performance.set_index("Month"))

# Distributor View
elif role == "Distributor":
    st.title("🔗 Distributor Dashboard")
    st.subheader("Sales Overview")

    st.metric("Total Clients Referred", 18)
    st.metric("Total AUM Raised", "₹ 22 Cr")

    st.subheader("Top Performing RMs")
    st.table(pd.DataFrame({
        "RM Name": ["Ravi", "Neha", "Arjun"],
        "Clients Added": [5, 4, 3],
        "AUM Raised (Cr)": [5.5, 4.2, 3.8]
    }))

# Investor View
elif role == "Investor":
    st.title("💼 Investor Dashboard")
    st.subheader("My Portfolio")

    my_portfolio = pd.DataFrame({
        "Asset": ["Equity", "Debt", "Cash"],
        "Value (₹ Lakhs)": [7.5, 3.0, 1.0]
    })

    st.dataframe(my_portfolio)
    st.subheader("Performance")
    st.line_chart(pd.DataFrame({
        "Month": pd.date_range("2024-01-01", periods=6, freq='M'),
        "Portfolio Value": [10, 10.5, 11.2, 11.0, 11.8, 12.3]
    }).set_index("Month"))

    st.subheader("My Advisor")
    st.info("Your RM: Neha Sharma (📧 neha@jane-pms.in)")
