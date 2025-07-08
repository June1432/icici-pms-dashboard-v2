import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="JANE PMS Dashboard", layout="wide")

# Custom CSS for Alloy-style professional theme (no emojis, clean layout)
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .block-container {
        padding: 2rem;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #111111 !important;
        border-radius: 12px;
        padding: 1rem;
    }
    .stMetric {
        color: #00f2ff;
    }
    </style>
""", unsafe_allow_html=True)

roles = ["Relationship Manager", "Fund Manager", "Distributor", "Investor"]
role = st.sidebar.selectbox("Select your role:", roles)

# Sidebar filter example
st.sidebar.markdown("---")
st.sidebar.text_input("Search by Name, PAN, City")
st.sidebar.selectbox("Filter by Risk Profile", ["All", "Low", "Medium", "High"])

# Dummy RM, FM, Distributor, Investor lists
rms = ["Ravi Mehta", "Neha Sharma", "Arjun Iyer", "Divya Rao", "Kunal Singh"]
fms = ["Rahul Khanna", "Sneha Desai", "Amit Verma", "Priya Das", "Vinay Joshi"]
distributors = ["Motilal", "NJ Wealth", "ICICI Direct", "Axis Capital", "Groww"]
investors = ["Investor A", "Investor B", "Investor C", "Investor D", "Investor E"]

# Simulated RM Data
def get_rm_data(name):
    return {
        "Total Clients": np.random.randint(10, 50),
        "AUM (Cr)": round(np.random.uniform(5, 50), 2),
        "Accounts": {
            "Q1": np.random.randint(1, 10),
            "Q2": np.random.randint(1, 10),
            "Q3": np.random.randint(1, 10),
            "Q4": np.random.randint(1, 10),
        },
        "Incentive Earned (₹ Lakhs)": round(np.random.uniform(1, 10), 2),
        "Successful Leads": np.random.randint(5, 20),
        "Unsuccessful Leads": np.random.randint(1, 10)
    }

# Simulated Distributor Data
def get_distributor_data(name):
    return {
        "Default Share Allocated (%)": round(np.random.uniform(10, 25), 2),
        "Business Brought (Cr)": round(np.random.uniform(5, 30), 2),
        "Business Lost (Cr)": round(np.random.uniform(0, 10), 2),
        "Clients": [
            {"Name": f"Client {i+1}", "AUM (Cr)": round(np.random.uniform(0.5, 5), 2), "Location": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai"])}
            for i in range(5)
        ]
    }

# Simulated FM Data
def get_fm_data(name):
    return {
        "Total Clients": np.random.randint(30, 100),
        "Total AUM (Cr)": round(np.random.uniform(100, 500), 2),
        "YTD P&L (%)": round(np.random.uniform(-5, 15), 2),
        "NAV (₹)": round(np.random.uniform(90, 150), 2)
    }

# Simulated Investor Data
def get_investor_data(name):
    return {
        "Total Value (₹ Lakhs)": round(np.random.uniform(5, 50), 2),
        "Daily P&L (₹)": round(np.random.uniform(-5000, 10000), 2),
        "Total P&L (₹)": round(np.random.uniform(-20000, 40000), 2),
        "Brokerage (₹)": round(np.random.uniform(100, 500), 2),
        "RM": np.random.choice(rms),
        "FM": np.random.choice(fms),
        "SM": np.random.choice(["Rohit Sinha", "Kiran Shetty"]),
        "Allocation": np.random.choice(["Equity Heavy", "Debt Balanced", "Hybrid"])
    }

if role == "Relationship Manager":
    st.title("Relationship Manager Dashboard")
    selected_rm = st.selectbox("Select RM:", rms)
    data = get_rm_data(selected_rm)
    st.subheader(f"Summary for {selected_rm}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", data["Total Clients"])
    col2.metric("AUM (Cr)", f"₹ {data['AUM (Cr)']}")
    col3.metric("Incentive Earned", f"₹ {data['Incentive Earned (₹ Lakhs)']} Lakhs")

    st.subheader("Quarter-wise Accounts Opened")
    account_df = pd.DataFrame.from_dict(data['Accounts'], orient='index', columns=["Accounts"])
    st.bar_chart(account_df)

    st.subheader("Lead Performance")
    lead_df = pd.DataFrame({
        "Lead Status": ["Successful", "Unsuccessful"],
        "Count": [data['Successful Leads'], data['Unsuccessful Leads']]
    })
    fig = px.pie(lead_df, values='Count', names='Lead Status', title="Lead Success Ratio")
    st.plotly_chart(fig, use_container_width=True)

elif role == "Distributor":
    st.title("Distributor Dashboard")
    selected_dist = st.selectbox("Select Distributor:", distributors)
    data = get_distributor_data(selected_dist)
    st.subheader(f"Summary for {selected_dist}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Default Share Allocated", f"{data['Default Share Allocated (%)']}%")
    col2.metric("Business Brought", f"₹ {data['Business Brought (Cr)']} Cr")
    col3.metric("Business Lost", f"₹ {data['Business Lost (Cr)']} Cr")

    st.subheader("Client Details")
    st.table(pd.DataFrame(data['Clients']))

elif role == "Fund Manager":
    st.title("Fund Manager Dashboard")
    selected_fm = st.selectbox("Select Fund Manager:", fms)
    data = get_fm_data(selected_fm)
    st.subheader(f"Summary for {selected_fm}")

    col1, col2 = st.columns(2)
    col1.metric("Total Clients", data["Total Clients"])
    col2.metric("Total AUM (Cr)", f"₹ {data['Total AUM (Cr)']}")

    col3, col4 = st.columns(2)
    col3.metric("YTD P&L (%)", f"{data['YTD P&L (%)']}%")
    col4.metric("NAV", f"₹ {data['NAV (₹)']}")

elif role == "Investor":
    st.title("Investor Dashboard")
    selected_inv = st.selectbox("Select Investor:", investors)
    data = get_investor_data(selected_inv)
    st.subheader(f"Summary for {selected_inv}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Value", f"₹ {data['Total Value (₹ Lakhs)']} Lakhs")
    col2.metric("Daily P&L", f"₹ {data['Daily P&L (₹)']}")
    col3.metric("Total P&L", f"₹ {data['Total P&L (₹)']}")

    st.metric("Brokerage Paid", f"₹ {data['Brokerage (₹)']}")

    st.subheader("Relationship Mapping")
    st.write({"Relationship Manager": data['RM'], "Fund Manager": data['FM'], "Senior Manager": data['SM']})
    st.write({"Portfolio Allocation": data['Allocation']})
