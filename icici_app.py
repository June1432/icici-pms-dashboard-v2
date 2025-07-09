# app.py – Simplified Streamlit App for GitHub Deployment
import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- App Setup ---
st.set_page_config(
    page_title="NAVIS | AMC Workflow",
    layout="wide"
)

# --- Sidebar Role Selector ---
st.sidebar.title("Login")
role = st.sidebar.selectbox("Select Your Role", [
    "Investor", "Relationship Manager", "Fund Manager", "Operations",
    "Compliance Officer", "Customer Support", "Fund Accounting",
    "Admin", "Auditor"
])

# --- Main Content ---
if role == "Investor":
    st.header("Investor Dashboard")
    portfolio = pd.DataFrame({
        "Scheme": ["Equity Fund", "Debt Fund", "Hybrid Fund"],
        "Value (₹ Lakhs)": [2.4, 1.5, 0.9],
        "Returns (%)": [12.3, 5.2, 7.8]
    })
    st.subheader("Portfolio Overview")
    st.dataframe(portfolio)
    st.subheader("Asset Allocation")
    st.plotly_chart(px.pie(portfolio, names="Scheme", values="Value (₹ Lakhs)"))
    st.subheader("Insights")
    st.info(random.choice([
        "Increase SIP in Equity Fund.",
        "Hybrid Fund underperforming, consider review.",
        "You are on track for your 5-year goal."
    ]))

elif role == "Relationship Manager":
    st.header("Relationship Manager Dashboard")
    st.metric("New Leads", 24)
    st.metric("KYC Pending", 5)
    st.metric("Active SIPs", 40)
    st.write(pd.DataFrame({
        "Investor": ["Raj", "Anita", "John"],
        "Status": ["Pending", "Approved", "In Review"]
    }))

elif role == "Fund Manager":
    st.header("Fund Manager Dashboard")
    st.write(pd.DataFrame({
        "Scheme": ["Growth Fund", "Income Fund"],
        "AUM (₹ Cr)": [520, 340],
        "YTD Return (%)": [8.2, 6.5]
    }))
    st.info("Growth Fund outperformed benchmark by 1.3%.")

elif role == "Operations":
    st.header("Operations Dashboard")
    st.success("Transactions Processed Today: 1,542")
    st.warning("Failed Transactions: 8")

elif role == "Compliance Officer":
    st.header("Compliance Dashboard")
    st.warning("2 STR alerts flagged today")
    st.info("All FATCA/CRS reports submitted")

elif role == "Customer Support":
    st.header("Customer Support Dashboard")
    st.write("Open Tickets: 12")
    st.write("Resolved Today: 18")

elif role == "Fund Accounting":
    st.header("Fund Accounting Dashboard")
    st.write("NAVs published for 18 schemes")
    st.download_button("Download NAV Report", "Sample NAV Report\nScheme,NAV\nGrowth Fund,102.56")

elif role == "Admin":
    st.header("Admin Dashboard")
    st.write("Active Users: 84")
    st.success("All access logs backed up")

elif role == "Auditor":
    st.header("Auditor Dashboard")
    st.write("Download logs for last 30 days")
    st.button("Generate Audit Report")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 NAVIS Mutual AMC")
