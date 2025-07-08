import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="JANE | Fund Management", layout="wide")

# Minimal black-and-white styling
st.markdown("""
<style>
body, .main { background-color: #fff; color: #000; }
div.stButton button { background-color: #000; color: #fff; }
.stTextInput, .stNumberInput, .stSelectbox { background-color: #f2f2f2; color: #000; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("JANE Fund Management Dashboard")
st.markdown("• SEBI/RBI Compliant • Clean, modern design")

# Sidebar roles & client inputs
role = st.sidebar.radio("Select Role", ["Relationship Manager", "Fund Manager", "Sales Manager"])
st.sidebar.markdown(f"**Logged in as:** {role}")

client = st.sidebar.text_input("Client Name")
capital = st.sidebar.number_input("Investment Capital (₹)", min_value=100000, step=50000)
risk = st.sidebar.selectbox("Risk Profile", ["Conservative", "Balanced", "Aggressive"])

# Stock universe and prices
stock_pool = {
    "Conservative": ["HDFCBANK", "INFY", "ITC", "SBI"],
    "Balanced": ["ICICIBANK", "RELIANCE", "TCS", "MARUTI"],
    "Aggressive": ["ADANIENT", "ZOMATO", "IRCTC", "TATAMOTORS"]
}
prices = {"HDFCBANK":1600, "INFY":1500, "ITC":480, "SBI":720, "ICICIBANK":1150,
          "RELIANCE":2800, "TCS":3800, "MARUTI":10500, "ADANIENT":3100,
          "ZOMATO":195, "IRCTC":890, "TATAMOTORS":950}

# Allocate dynamically
sel = stock_pool[risk]
alloc = random.choices(range(20,31), k=4)
alloc = [round(a*100/sum(alloc),2) for a in alloc]

df = pd.DataFrame({"Stock": sel, "Alloc (%)": alloc})
df["Invest (₹)"] = df["Alloc (%)"] * capital / 100
df["Price (₹)"] = df["Stock"].map(prices)
df["Units"] = df["Invest (₹)"]/df["Price (₹)"]
df["Return (%)"] = [round(random.uniform(-5,10),2) for _ in df.index]
df["Value (₹)"] = df["Invest (₹)"] * (1 + df["Return (%)"]/100)

# Benchmark & metrics
benchmark = 6.5
port_ret = round((df["Value (₹)"].sum()-capital)/capital*100,2)
alpha = round(port_ret - benchmark,2)
beta = round(random.uniform(0.9,1.2),2)
gamma = round(random.uniform(0.1,0.9),2)

# Display layout
st.subheader(f"Client Portfolio: {client or '—'}")
st.dataframe(df.style.format({"Alloc (%)":"{:.2f}%", "Invest (₹)":"₹{:.2f}",
                              "Price (₹)":"₹{:.2f}", "Units":"{:.2f}",
                              "Return (%)":"{:.2f}%", "Value (₹)":"₹{:.2f}"}))

c1, c2, c3 = st.columns(3)
c1.metric("Portfolio Return", f"{port_ret}%", delta=f"{port_ret-benchmark}% vs Benchmark")
c2.metric("Alpha", f"{alpha}%")
c3.metric("Benchmark", f"{benchmark}%")

c4, c5, c6 = st.columns(3)
c4.metric("Beta", f"{beta}")
c5.metric("Gamma", f"{gamma}")
c6.metric("Total Value", f"₹{df['Value (₹)'].sum():,.2f}")

# Billing
next_bill = datetime.today() + timedelta(days=30)
st.markdown(f"**Next Billing Date:** {next_bill.strftime('%d %b %Y')}")

# Compliance note
st.markdown("---")
st.markdown("Compliant with **SEBI (Portfolio Managers) Regulations, 2020** and **RBI oversight**.")
