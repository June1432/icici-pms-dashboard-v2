import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="JANE PMS Dashboard", layout="wide")

# Black & White enterprise theme
st.markdown("""
    <style>
    body, .stApp {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
    .stMetric, .stText, .stHeader {
        color: #000000;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #f4f4f4 !important;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

roles = ["Relationship Manager", "Fund Manager", "Service Manager", "Distributor"]
role = st.sidebar.selectbox("Select User Role:", roles)

# Sidebar filters
st.sidebar.text_input("Search Client (Name / PAN / City):")
st.sidebar.selectbox("Filter by Risk Profile:", ["All", "Low", "Medium", "High"])

# Dummy user pools
rms = ["Ravi Mehta", "Neha Sharma", "Arjun Iyer", "Divya Rao", "Kunal Singh"]
fms = ["Rahul Khanna", "Sneha Desai", "Amit Verma", "Priya Das", "Vinay Joshi"]
distributors = ["Motilal", "NJ Wealth", "ICICI Direct", "Axis Capital", "Groww"]
clients = [f"Client {i}" for i in range(1, 6)]

# Simulation functions
def get_client_data():
    return pd.DataFrame({
        "Client ID": [f"CID{i}" for i in range(1, 6)],
        "Name": clients,
        "Capital (₹ Lakhs)": np.random.randint(10, 100, size=5),
        "Risk Profile": np.random.choice(["Low", "Medium", "High"], size=5),
        "Strategy": np.random.choice(["Value", "Growth", "Momentum"], size=5),
        "NAV": np.round(np.random.uniform(90, 150, 5), 2),
        "TWR (%)": np.round(np.random.uniform(-2, 15, 5), 2),
        "MWR (%)": np.round(np.random.uniform(-2, 18, 5), 2),
        "Custodian": np.random.choice(["HDFC Bank", "ICICI Bank"], size=5),
        "Bank Account": [f"XXXX{i}1234" for i in range(5)],
        "PEP": np.random.choice(["Yes", "No"], size=5),
        "PIS No": [f"PIS00{i}" for i in range(5)],
        "Country": np.random.choice(["India", "UAE", "Singapore", "UK"], size=5),
        "FM": np.random.choice(fms, size=5),
        "RM": np.random.choice(rms, size=5),
        "SM": np.random.choice(["Rohit Sinha", "Kiran Shetty"], size=5)
    })

def calculate_ratios(row, rf=0.05, beta=1.0, mr=0.12):
    try:
        returns = row['TWR (%)'] / 100
        volatility = 0.12
        sharpe = (returns - rf) / volatility
        treynor = (returns - rf) / beta
        jensen = returns - (rf + beta * (mr - rf))
        return pd.Series([sharpe, treynor, jensen])
    except:
        return pd.Series([None, None, None])

client_data = get_client_data()
client_data[['Sharpe', 'Treynor', 'Jensen']] = client_data.apply(calculate_ratios, axis=1)

if role == "Fund Manager":
    st.title("Fund Manager Dashboard")
    st.subheader("Managed Clients Overview")
    st.dataframe(client_data[["Client ID", "Name", "Capital (₹ Lakhs)", "Strategy", "NAV", "TWR (%)", "MWR (%)"]])
    st.subheader("Strategy Insights")
    st.bar_chart(client_data['Strategy'].value_counts())

elif role == "Relationship Manager":
    st.title("Relationship Manager Dashboard")
    st.subheader("Client Portfolio Overview")
    st.dataframe(client_data[["Client ID", "Name", "Capital (₹ Lakhs)", "Risk Profile", "NAV", "TWR (%)", "MWR (%)"]])

elif role == "Service Manager":
    st.title("Service Manager View")
    st.subheader("Client Assignment")
    st.dataframe(client_data[["Client ID", "Name", "RM", "FM", "SM", "Custodian", "Bank Account", "PEP", "Country", "PIS No"]])

elif role == "Distributor":
    st.title("Distributor Dashboard")
    st.subheader("Client Distribution Overview")
    st.dataframe(client_data[["Client ID", "Name", "Capital (₹ Lakhs)", "Strategy", "Country"]])
