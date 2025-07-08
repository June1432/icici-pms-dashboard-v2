# alloy_pms_dashboard.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Alloy-Inspired PMS Dashboard", layout="wide")

# -------------------------------
# Header and Role
# -------------------------------
st.title("📈 Portfolio Management Dashboard (Alloy Style)")
role = st.sidebar.selectbox("Your Role", ["Relationship Manager (RM)", "Fund Manager (FM)", "Sales Manager (SM)"])

st.sidebar.markdown(f"🧑 Logged in as **{role}**")

client_name = st.text_input("Enter Client Name:")
capital = st.number_input("Investment Capital (₹)", min_value=100000, step=50000)
risk_profile = st.radio("Select Risk Profile", ["Conservative", "Balanced", "Aggressive"])

# -------------------------------
# Dummy Indian stock universe
# -------------------------------
stock_pool = {
    "Conservative": ["HDFCBANK", "INFY", "ITC", "SBI"],
    "Balanced": ["ICICIBANK", "RELIANCE", "TCS", "MARUTI"],
    "Aggressive": ["ADANIENT", "ZOMATO", "IRCTC", "TATAMOTORS"]
}

stock_prices = {
    "HDFCBANK": 1600, "INFY": 1500, "ITC": 480, "SBI": 720,
    "ICICIBANK": 1150, "RELIANCE": 2800, "TCS": 3800, "MARUTI": 10500,
    "ADANIENT": 3100, "ZOMATO": 195, "IRCTC": 890, "TATAMOTORS": 950
}

benchmark_price_today = 22000  # e.g., Nifty 50
benchmark_price_30_days_ago = 21200
benchmark_return = round(((benchmark_price_today - benchmark_price_30_days_ago) / benchmark_price_30_days_ago) * 100, 2)

# -------------------------------
# Portfolio Allocation
# -------------------------------
selected_stocks = stock_pool[risk_profile]
allocations = [random.randint(20, 30) for _ in range(4)]
allocations = [round(x * (100 / sum(allocations)), 2) for x in allocations]

data = {
    "Stock": selected_stocks,
    "Allocation (%)": allocations
}
df = pd.DataFrame(data)
df["Investment (₹)"] = (df["Allocation (%)"] * capital) / 100
df["Price (₹)"] = df["Stock"].map(stock_prices)
df["Units"] = df["Investment (₹)"] / df["Price (₹)"]

# -------------------------------
# Returns Simulation
# -------------------------------
df["Return (%)"] = [round(random.uniform(-5, 12), 2) for _ in range(4)]
df["Current Value"] = df["Investment (₹)"] * (1 + df["Return (%)"] / 100)

# -------------------------------
# Metrics Calculation
# -------------------------------
portfolio_return = ((df["Current Value"].sum() - capital) / capital) * 100
alpha = round(portfolio_return - benchmark_return, 2)
beta = round(random.uniform(0.85, 1.2), 2)
gamma = round(random.uniform(0.1, 0.9), 2)

# -------------------------------
# Display Section
# -------------------------------
st.subheader(f"📊 Portfolio Overview for {client_name if client_name else 'Investor'}")
st.dataframe(df.style.format({
    "Allocation (%)": "{:.2f}%",
    "Investment (₹)": "₹{:.2f}",
    "Price (₹)": "₹{:.2f}",
    "Units": "{:.2f}",
    "Return (%)": "{:.2f}%",
    "Current Value": "₹{:.2f}"
}))

# -------------------------------
# Key Metrics
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("📈 Portfolio Return", f"{portfolio_return:.2f}%", delta=f"{portfolio_return - benchmark_return:.2f}% vs Benchmark")
col2.metric("📊 Alpha", f"{alpha}%")
col3.metric("📉 Benchmark Return", f"{benchmark_return}%")

col4, col5, col6 = st.columns(3)
col4.metric("📐 Beta", f"{beta}")
col5.metric("📶 Gamma", f"{gamma}")
col6.metric("🧾 Total Value", f"₹{df['Current Value'].sum():,.2f}")

# -------------------------------
# Billing Info
# -------------------------------
next_billing_date = datetime.today() + timedelta(days=30)
st.info(f"📅 Next Billing Date: **{next_billing_date.strftime('%d %B %Y')}**")

