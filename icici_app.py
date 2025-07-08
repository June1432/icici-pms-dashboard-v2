import streamlit as st
import graphviz
import pandas as pd
import numpy as np
import datetime
from io import BytesIO

st.set_page_config(page_title="JANE PMS Dashboard", layout="wide")

st.title("JANE | AMC Client Lifecycle Workflow")
st.markdown("Designed for internal operations, compliance, and investment teams.")

st.subheader("Client Lifecycle: Prospect to Closure")

workflow = graphviz.Digraph()
workflow.attr(rankdir="LR", fontsize="10")

workflow.node("Prospect", "Prospect (HNI / Institution)", shape="box")
workflow.node("Sales", "Sales / RM / Distributor", shape="box")
workflow.edge("Prospect", "Sales", label="Lead Generation")
workflow.edge("Sales", "Compliance", label="KYC & Due Diligence")

workflow.node("Compliance", "Compliance & Legal", shape="box")
workflow.node("Operations", "Operations Team", shape="box")
workflow.edge("Compliance", "Operations", label="Data Verification")
workflow.edge("Operations", "ClientLogin", label="Portal & Dashboard Setup")
workflow.node("ClientLogin", "Client Login Created", shape="box")

workflow.node("FundManager", "Fund Manager (FM)", shape="box")
workflow.node("TradeDesk", "Trade Desk", shape="box")
workflow.edge("ClientLogin", "FundManager", label="Capital Allocation")
workflow.edge("FundManager", "TradeDesk", label="Strategy → Execution")
workflow.edge("TradeDesk", "Operations", label="Execution / Units Allocated")

workflow.node("Monitoring", "Monitoring & Reporting", shape="box")
workflow.node("Client", "Client", shape="box")
workflow.edge("Operations", "Monitoring", label="NAV / TWR Feeds")
workflow.edge("Monitoring", "Client", label="Statements / Commentary")

workflow.node("RMUpdate", "Relationship Manager", shape="box")
workflow.edge("Client", "RMUpdate", label="Top-Up / Exit / Strategy Change")
workflow.edge("RMUpdate", "FundManager", label="Rebalance Instruction")
workflow.edge("FundManager", "TradeDesk")
workflow.edge("TradeDesk", "Operations")
workflow.edge("Operations", "Monitoring")

workflow.node("Finance", "Finance Team", shape="box")
workflow.node("Exit", "Exit & Closure", shape="box")
workflow.edge("Client", "Exit", label="Full Redemption")
workflow.edge("Exit", "Operations", label="Liquidation Process")
workflow.edge("Operations", "Finance", label="Payout Processing")
workflow.edge("Finance", "Client", label="Payout + Final Report")

st.graphviz_chart(workflow)

st.markdown("---")
st.sidebar.title("Select Role View")
role = st.sidebar.selectbox("User Role:", ["Fund Manager", "Relationship Manager", "Service Manager", "Distributor"])

rms = ["Ravi Mehta", "Neha Sharma", "Arjun Iyer", "Divya Rao", "Kunal Singh"]
fms = ["Rahul Khanna", "Sneha Desai", "Amit Verma", "Priya Das", "Vinay Joshi"]
distributors = ["Motilal", "NJ Wealth", "ICICI Direct", "Axis Capital", "Groww"]
clients = [f"Client {i}" for i in range(1, 11)]

@st.cache_data
def get_client_data():
    start_dates = [datetime.date(2023, 1, i+1) for i in range(10)]
    end_dates = [datetime.date(2025, 1, i+1) for i in range(10)]
    return pd.DataFrame({
        "Client ID": [f"CID{i}" for i in range(1, 11)],
        "Name": clients,
        "Capital (₹ Lakhs)": np.random.randint(10, 100, size=10),
        "Risk Profile": np.random.choice(["Low", "Medium", "High"], size=10),
        "Strategy": np.random.choice(["Value", "Growth", "Momentum"], size=10),
        "NAV": np.round(np.random.uniform(90, 150, 10), 2),
        "TWR (%)": np.round(np.random.uniform(-2, 15, 10), 2),
        "MWR (%)": np.round(np.random.uniform(-2, 18, 10), 2),
        "Start Date": start_dates,
        "End Date": end_dates,
        "Custodian": np.random.choice(["HDFC Bank", "ICICI Bank"], size=10),
        "Bank Account": [f"XXXX{i}1234" for i in range(10)],
        "PEP": np.random.choice(["Yes", "No"], size=10),
        "PIS No": [f"PIS00{i}" for i in range(10)],
        "Country": np.random.choice(["India", "UAE", "Singapore", "UK"], size=10),
        "FM": np.random.choice(fms, size=10),
        "RM": np.random.choice(rms, size=10),
        "SM": np.random.choice(["Rohit Sinha", "Kiran Shetty"], size=10),
        "Distributor": np.random.choice(distributors, size=10)
    })

def calculate_ratios(row, rf=0.05, beta=1.0, mr=0.12):
    returns = row['TWR (%)'] / 100
    volatility = 0.12
    sharpe = (returns - rf) / volatility
    treynor = (returns - rf) / beta
    jensen = returns - (rf + beta * (mr - rf))
    return pd.Series({'Sharpe': sharpe, 'Treynor': treynor, 'Jensen': jensen})

def calculate_irr(row):
    try:
        cashflows = [-row['Capital (₹ Lakhs)']] + [row['NAV'] / 12] * 24
        return np.irr(cashflows)
    except:
        return None

client_data = get_client_data()
client_data[['Sharpe', 'Treynor', 'Jensen']] = client_data.apply(calculate_ratios, axis=1)
client_data['IRR'] = client_data.apply(calculate_irr, axis=1)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

if role == "Fund Manager":
    selected_fm = st.selectbox("Select Fund Manager:", fms)
    fm_clients = client_data[client_data['FM'] == selected_fm]
    st.title(f"Fund Manager View - {selected_fm}")
    st.metric("Total AUM (₹ Cr)", f"{fm_clients['Capital (₹ Lakhs)'].sum() / 100:.2f}")
    st.bar_chart(fm_clients.set_index("Name")["Capital (₹ Lakhs)"])
    st.subheader("Strategy Breakdown")
    st.bar_chart(fm_clients['Strategy'].value_counts())
    st.subheader("NAV vs Benchmark")
    st.line_chart(fm_clients.set_index("Name")[["NAV", "TWR (%)"]])
    st.metric("Benchmark Return (Nifty 1Y)", "12.0%")
    st.download_button("Download FM Data (Excel)", data=to_excel(fm_clients), file_name="FM_Report.xlsx")

elif role == "Relationship Manager":
    selected_rm = st.selectbox("Select RM:", rms)
    rm_clients = client_data[client_data['RM'] == selected_rm]
    st.title(f"Relationship Manager View - {selected_rm}")
    st.bar_chart(rm_clients['Risk Profile'].value_counts())
    st.subheader("Capital by Client")
    st.bar_chart(rm_clients.set_index("Name")["Capital (₹ Lakhs)"])
    st.subheader("Assigned Clients")
    st.dataframe(rm_clients[["Client ID", "Name", "Strategy", "Risk Profile", "TWR (%)", "NAV", "IRR"]])
    st.download_button("Download RM Dat
