# icici_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="ICICI PMS Dashboard", layout="wide")

st.sidebar.markdown("👤 Logged in as **ICICI PMS** Portfolio Manager")

st.title("📊 ICICI Portfolio Management Dashboard")
st.markdown("Simulated PMS-like interface for Indian investors")

client_name = st.text_input("Enter Client Name:")
capital = st.number_input("Enter Investment Capital (₹):", min_value=100000, step=10000)
risk_profile = st.selectbox("Select Risk Profile", ["Conservative", "Balanced", "Aggressive"])

def get_dummy_stocks(risk):
    if risk == "Conservative":
        return {
            "HDFCBANK": 25,
            "INFY": 25,
            "ITC": 25,
            "SBI": 25
        }
    elif risk == "Balanced":
        return {
            "ICICIBANK": 30,
            "RELIANCE": 30,
            "TCS": 20,
            "MARUTI": 20
        }
    else:
        return {
            "ADANIENT": 40,
            "ZOMATO": 20,
            "IRCTC": 20,
            "TATAMOTORS": 20
        }

stock_data = {
    "HDFCBANK": {"price": 1600, "dividend": 15},
    "INFY": {"price": 1500, "dividend": 10},
    "ITC": {"price": 480, "dividend": 20},
    "SBI": {"price": 720, "dividend": 12},
    "ICICIBANK": {"price": 1150, "dividend": 10},
    "RELIANCE": {"price": 2800, "dividend": 25},
    "TCS": {"price": 3800, "dividend": 22},
    "MARUTI": {"price": 10500, "dividend": 40},
    "ADANIENT": {"price": 3100, "dividend": 0},
    "ZOMATO": {"price": 195, "dividend": 0},
    "IRCTC": {"price": 890, "dividend": 8},
    "TATAMOTORS": {"price": 950, "dividend": 7}
}

portfolio = get_dummy_stocks(risk_profile)

df = pd.DataFrame(portfolio.items(), columns=["Stock", "Allocation (%)"])
df["Investment (₹)"] = df["Allocation (%)"] * capital / 100
df["Stock Price (₹)"] = df["Stock"].map(lambda x: stock_data[x]["price"])
df["Units"] = df["Investment (₹)"] / df["Stock Price (₹)"]
df["Dividend/Unit (₹)"] = df["Stock"].map(lambda x: stock_data[x]["dividend"])
df["Total Dividend"] = df["Units"] * df["Dividend/Unit (₹)"]
df["TDS (10%)"] = df["Total Dividend"] * 0.10

transactions = len(df)
brokerage_fee = transactions * 10

def simulate_returns():
    daily = round(random.uniform(-0.5, 0.5), 2)
    weekly = round(random.uniform(-1.5, 1.5), 2)
    monthly = round(random.uniform(-4, 4), 2)
    return daily, weekly, monthly

daily_ret, weekly_ret, monthly_ret = simulate_returns()

nav = capital + (monthly_ret / 100) * capital
total_dividend = df["Total Dividend"].sum()
total_tds = df["TDS (10%)"].sum()

alpha = round(random.uniform(1, 5), 2)
beta = round(random.uniform(0.7, 1.3), 2)
gamma = round(random.uniform(0.1, 1.0), 2)

st.subheader("📈 Portfolio Overview")
st.dataframe(df.style.format({"Investment (₹)": "₹{:.2f}", "Stock Price (₹)": "₹{:.2f}", 
                              "Units": "{:.2f}", "Total Dividend": "₹{:.2f}", "TDS (10%)": "₹{:.2f}"}))

col1, col2, col3 = st.columns(3)
col1.metric("💹 NAV", f"₹{nav:,.2f}")
col2.metric("🎁 Dividends", f"₹{total_dividend:,.2f}")
col3.metric("🧾 TDS", f"₹{total_tds:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("📆 Daily Return (%)", f"{daily_ret}%")
col5.metric("🗓️ Weekly Return (%)", f"{weekly_ret}%")
col6.metric("📅 Monthly Return (%)", f"{monthly_ret}%")

col7, col8, col9 = st.columns(3)
col7.metric("📊 Alpha", f"{alpha}")
col8.metric("📊 Beta", f"{beta}")
col9.metric("📊 Gamma", f"{gamma}")

st.write(f"💸 Total Brokerage Charged: ₹{brokerage_fee}")
billing_date = datetime.today() + timedelta(days=30)
st.write(f"🧾 Next Billing Date: {billing_date.strftime('%d %B %Y')}")

st.subheader("🏢 Other PMS Providers in India")
pms_list = [
    "Motilal Oswal PMS",
    "Marcellus Investment Managers",
    "ASK Investment Managers",
    "SBI PMS",
    "White Oak Capital",
    "Aditya Birla PMS"
]
for pms in pms_list:
    st.markdown(f"- {pms}")
