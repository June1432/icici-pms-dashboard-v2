import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="JANE PMS Dashboard", layout="wide")

# Light theme custom styling (clean, professional)
st.markdown("""
    <style>
    body, .stApp {
        background-color: #f7f7f9;
        color: #000000;
    }
    .block-container {
        padding: 2rem;
    }
    .stMetric {
        color: #004080;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 0 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

roles = ["Relationship Manager", "Fund Manager", "Distributor", "Investor"]
role = st.sidebar.selectbox("Select User Role:", roles)

st.sidebar.markdown("---")
st.sidebar.text_input("Search Client (Name / PAN / City):")
st.sidebar.selectbox("Filter by Risk Profile:", ["All", "Low", "Medium", "High"])

# Dummy user data
rms = ["Ravi Mehta", "Neha Sharma", "Arjun Iyer", "Divya Rao", "Kunal Singh"]
fms = ["Rahul Khanna", "Sneha Desai", "Amit Verma", "Priya Das", "Vinay Joshi"]
distributors = ["Motilal", "NJ Wealth", "ICICI Direct", "Axis Capital", "Groww"]
investors = ["Investor A", "Investor B", "Investor C", "Investor D", "Investor E"]

# Utility Ratios
ratio_guide = pd.DataFrame({
    "Ratio": ["Sharpe Ratio", "Treynor Ratio", "Jensen Alpha"],
    "Best Used By": ["Retail investors, Analysts, PMS Advisors", "Institutional Investors", "HNIs, Portfolio Evaluators"],
    "Definition": [
        "Return per unit of total risk (Volatility)",
        "Return per unit of systematic risk (Beta-based)",
        "Excess return above market due to manager skill"
    ]
})

# Simulated RM Data
def get_rm_data(name):
    return {
        "Total Clients": np.random.randint(10, 50),
        "Assets Under Management (₹ Cr)": round(np.random.uniform(5, 50), 2),
        "Accounts": {
            "Q1": np.random.randint(1, 10),
            "Q2": np.random.randint(1, 10),
            "Q3": np.random.randint(1, 10),
            "Q4": np.random.randint(1, 10),
        },
        "Incentive Earned (₹ Lakhs)": round(np.random.uniform(1, 10), 2),
        "Leads": {
            "Converted": np.random.randint(5, 20),
            "Dropped": np.random.randint(1, 10)
        }
    }

# Simulated Distributor Data
def get_distributor_data(name):
    return {
        "Default Allocation (%)": round(np.random.uniform(10, 25), 2),
        "Business Generated (₹ Cr)": round(np.random.uniform(5, 30), 2),
        "Business Lost (₹ Cr)": round(np.random.uniform(0, 10), 2),
        "Clients": [
            {"Client Name": f"Client {i+1}", "AUM (₹ Cr)": round(np.random.uniform(0.5, 5), 2), "Location": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai"])}
            for i in range(5)
        ]
    }

# Simulated FM Data
def get_fm_data(name):
    return {
        "Managed Clients": np.random.randint(30, 100),
        "Total AUM (₹ Cr)": round(np.random.uniform(100, 500), 2),
        "Year-to-Date Performance (%)": round(np.random.uniform(-5, 15), 2),
        "Net Asset Value (₹)": round(np.random.uniform(90, 150), 2)
    }

# Simulated Investor Data
def get_investor_data(name):
    return {
        "Portfolio Value (₹ Lakhs)": round(np.random.uniform(5, 50), 2),
        "Daily MTM (₹)": round(np.random.uniform(-5000, 10000), 2),
        "Cumulative P&L (₹)": round(np.random.uniform(-20000, 40000), 2),
        "Total Brokerage (₹)": round(np.random.uniform(100, 500), 2),
        "Assigned RM": np.random.choice(rms),
        "Assigned FM": np.random.choice(fms),
        "Senior Manager": np.random.choice(["Rohit Sinha", "Kiran Shetty"]),
        "Asset Allocation": np.random.choice(["Equity-Oriented", "Debt-Focused", "Balanced"])
    }

if role == "Relationship Manager":
    st.title("Relationship Manager Portal")
    selected_rm = st.selectbox("Select Relationship Manager:", rms)
    data = get_rm_data(selected_rm)
    st.subheader(f"Performance Overview: {selected_rm}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", data["Total Clients"])
    col2.metric("Assets Under Management", f"₹ {data['Assets Under Management (₹ Cr)']} Cr")
    col3.metric("Incentive Earned", f"₹ {data['Incentive Earned (₹ Lakhs)']} Lakhs")

    st.subheader("Account Openings (Quarter-wise)")
    st.bar_chart(pd.DataFrame.from_dict(data['Accounts'], orient='index', columns=["New Accounts"]))

    st.subheader("Lead Conversion")
    lead_data = pd.DataFrame({
        "Lead Status": ["Converted", "Dropped"],
        "Count": [data['Leads']['Converted'], data['Leads']['Dropped']]
    })
    st.plotly_chart(px.pie(lead_data, values='Count', names='Lead Status', title="Lead Conversion Ratio"), use_container_width=True)

elif role == "Investor":
    def calculate_financial_ratios(data, risk_free_rate=0.05, beta=1.0, market_return=0.12):
        try:
            portfolio_value = data['Portfolio Value (₹ Lakhs)'] * 100000
            portfolio_return = data['Cumulative P&L (₹)'] / portfolio_value
            volatility = abs(data['Daily MTM (₹)']) / portfolio_value

            sharpe_ratio = (portfolio_return - risk_free_rate) / volatility if volatility else None
            treynor_ratio = (portfolio_return - risk_free_rate) / beta if beta else None
            jensen_alpha = portfolio_return - (risk_free_rate + beta * (market_return - risk_free_rate))

            return {
                "Sharpe Ratio": round(sharpe_ratio, 3) if sharpe_ratio else "N/A",
                "Treynor Ratio": round(treynor_ratio, 3) if treynor_ratio else "N/A",
                "Jensen Alpha": round(jensen_alpha, 3)
            }
        except ZeroDivisionError:
            return {
                "Sharpe Ratio": "N/A",
                "Treynor Ratio": "N/A",
                "Jensen Alpha": "N/A"
            }

    st.title("Investor Portfolio")
    selected_inv = st.selectbox("Select Investor:", investors)
    data = get_investor_data(selected_inv)
    st.subheader(f"Portfolio Overview: {selected_inv}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Portfolio Value", f"₹ {data['Portfolio Value (₹ Lakhs)']} Lakhs")
    col2.metric("Daily MTM", f"₹ {data['Daily MTM (₹)']}")
    col3.metric("Cumulative P&L", f"₹ {data['Cumulative P&L (₹)']}")

    st.metric("Brokerage Paid", f"₹ {data['Total Brokerage (₹)']}")

    st.subheader("Risk-Adjusted Performance Ratios")
    ratios = calculate_financial_ratios(data)
    colr1, colr2, colr3 = st.columns(3)
    colr1.metric("Sharpe Ratio", ratios['Sharpe Ratio'])
    colr2.metric("Treynor Ratio", ratios['Treynor Ratio'])
    colr3.metric("Jensen Alpha", ratios['Jensen Alpha'])

    st.subheader("Assigned Team & Strategy")
    st.write({
        "Relationship Manager": data['Assigned RM'],
        "Fund Manager": data['Assigned FM'],
        "Senior Manager": data['Senior Manager'],
        "Portfolio Allocation": data['Asset Allocation']
    })
