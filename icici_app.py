import streamlit as st
import graphviz

st.set_page_config(page_title="AMC Workflow | JANE", layout="wide")
st.title("JANE | AMC Client Lifecycle Workflow")
st.markdown("Designed for internal operations teams and onboarding staff")

st.subheader("🔄 Full Client Journey from Prospect to Exit")

# Graphviz Diagram
workflow = graphviz.Digraph()

# Stage 1: Lead
workflow.node("Prospect", "Prospect (HNI / Institution)", shape="box")
workflow.node("Sales", "Sales / RM / Distributor", shape="box")
workflow.edge("Prospect", "Sales", label="Lead generation")
workflow.edge("Sales", "Compliance", label="KYC / Due Diligence")

# Stage 2: Onboarding
workflow.node("Compliance", "Compliance & Legal", shape="box")
workflow.node("Operations", "Operations Team", shape="box")
workflow.edge("Compliance", "Operations", label="Verified client data")
workflow.edge("Operations", "ClientLogin", label="Create login & dashboard")
workflow.node("ClientLogin", "Client Login Created", shape="box")

# Stage 3: Portfolio Setup
workflow.node("FundManager", "Fund Manager (FM)", shape="box")
workflow.node("TradeDesk", "Trade Desk", shape="box")
workflow.edge("ClientLogin", "FundManager", label="Capital & risk profile")
workflow.edge("FundManager", "TradeDesk", label="Strategy → Execution")
workflow.edge("TradeDesk", "Operations", label="Units allocated")

# Stage 4: Monitoring
workflow.node("Monitoring", "Monitoring & Reporting", shape="box")
workflow.node("Client", "Client", shape="box")
workflow.edge("Operations", "Monitoring", label="NAV / TWR updates")
workflow.edge("Monitoring", "Client", label="Statements / Commentary")

# Stage 5: Modifications
workflow.node("RMUpdate", "Client RM / Servicing", shape="box")
workflow.edge("Client", "RMUpdate", label="Top-up / Exit / Strategy change")
workflow.edge("RMUpdate", "FundManager", label="Rebalance required")
workflow.edge("FundManager", "TradeDesk")
workflow.edge("TradeDesk", "Operations")
workflow.edge("Operations", "Monitoring")

# Stage 6: Exit
workflow.node("Finance", "Finance Team", shape="box")
workflow.node("Exit", "Exit & Closure", shape="box")
workflow.edge("Client", "Exit", label="Full withdrawal")
workflow.edge("Exit", "Operations", label="Liquidation")
workflow.edge("Operations", "Finance", label="Payout")
workflow.edge("Finance", "Client", label="Bank Transfer + Final Report")

# Display
st.graphviz_chart(workflow)

st.markdown("---")
st.markdown("**All processes comply with SEBI PMS Regulations, RBI KYC norms, and internal audit controls.")
