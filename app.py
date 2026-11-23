"""
Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines
Student: Veerparam Chauhan | Enrolment Number: PGD202563340
Industry:  Airline | Company: Delta Air Lines

Main Application File: app.py
Built with Streamlit, Pandas, and Python.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import storage
import rules
from gatekeeper import AgentGatekeeper

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agent Gatekeeper – Delta Air Lines",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize demonstration storage if completely empty
storage.init_default_data_if_empty()

# -----------------------------------------------------------------------------
# CUSTOM CSS – DELTA AIR LINES PROFESSIONAL PALETTE
# Navy Blue (#002244), Delta Red (#E01933), Light Slate Grey (#F4F6F9), White (#FFF)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header Container */
    .delta-header {
        background: linear-gradient(135deg, #002244 0%, #0B3B60 100%);
        color: #FFFFFF;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0, 34, 68, 0.15);
        border-bottom: 4px solid #E01933;
    }
    .delta-title {
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        color: #FFFFFF;
    }
    .delta-subtitle {
        font-size: 14px;
        color: #E2E8F0;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .badge-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }
    .student-badge {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: 500;
        color: #F1F5F9;
    }
    .disclaimer-badge {
        background: rgba(224, 25, 51, 0.2);
        border: 1px solid #E01933;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 500;
        color: #FECDD3;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #002244;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
    }

    /* Decision Result Box */
    .decision-box {
        border-radius: 10px;
        padding: 20px 24px;
        margin: 18px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .decision-allow {
        background-color: #F0FDF4;
        border-left: 6px solid #10B981;
        border: 1px solid #BBF7D0;
        border-left-width: 6px;
    }
    .decision-ask {
        background-color: #FFFBEB;
        border-left: 6px solid #F59E0B;
        border: 1px solid #FDE68A;
        border-left-width: 6px;
    }
    .decision-block {
        background-color: #FEF2F2;
        border-left: 6px solid #EF4444;
        border: 1px solid #FECACA;
        border-left-width: 6px;
    }
    .decision-header {
        font-size: 20px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .status-pill {
        font-size: 12px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }
    .pill-allow {
        background-color: #D1FAE5;
        color: #065F46;
    }
    .pill-ask {
        background-color: #FEF3C7;
        color: #92400E;
    }
    .pill-block {
        background-color: #FEE2E2;
        color: #991B1B;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="delta-header">
    <div class="delta-title">✈️ Agent Gatekeeper – AI Agent Permission and Access Control System</div>
    <div class="delta-subtitle">Selected Industry: Airline &bull; Selected Company: Delta Air Lines</div>
    <div class="badge-bar">
        <span class="student-badge">👤 Student: <b>Veerparam Chauhan</b></span>
        <span class="student-badge">🆔 Enrolment No: <b>PGD202563340</b></span>
        <span class="student-badge">🎓 Program: MBA Individual Assignment</span>
        <span class="disclaimer-badge">⚠️ Academic Prototype & Simulation (Not an official Delta Air Lines product)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Delta_logo.svg/320px-Delta_logo.svg.png", width=160)
    st.markdown("### **Navigation**")
    nav_selection = st.radio(
        "Select Module:",
        [
            "📊 Dashboard & Overview",
            "📝 Register AI Agent",
            "🛡️ Check Agent Request",
            "🚫 Revoke AI Agent",
            "📜 Immutable Audit Trail",
            "🧪 Automated Test Runner",
            "📚 Academic Context & Sources"
        ],
        index=0
    )
    st.markdown("---")
    st.markdown("""
    **Quick Reference:**
    - **R1:** Unknown Agent (BLOCK)
    - **R2:** Revoked Agent (BLOCK)
    - **R3:** Identity Mismatch (BLOCK)
    - **R4:** View Fares (ALLOW)
    - **R5:** Book Flight (≤$100 ALLOW, >$100 ASK)
    - **R6:** Change Flight (ASK CUSTOMER)
    - **R7:** Request Refund (ASK CUSTOMER)
    - **R8:** Unauthorized/Invalid (BLOCK)
    """)
    st.markdown("---")
    st.caption("Agent Gatekeeper v1.0 • Delta Air Lines MBA Prototype")

# Initialize Gatekeeper instance
gatekeeper = AgentGatekeeper()


# =============================================================================
# MODULE 1: DASHBOARD & OVERVIEW
# =============================================================================
if nav_selection == "📊 Dashboard & Overview":
    st.subheader("System Performance & Access Control Dashboard")

    metrics = storage.get_metrics()

    # Metric Row 1: Agents
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Registered Agents</div>
            <div class="metric-value">{metrics['total_agents']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Agents</div>
            <div class="metric-value" style="color: #10B981;">{metrics['active_agents']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Revoked Agents</div>
            <div class="metric-value" style="color: #EF4444;">{metrics['revoked_agents']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Evaluated Requests</div>
            <div class="metric-value">{metrics['total_requests']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Metric Row 2: Decisions Breakdown
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #10B981;">
            <div class="metric-label">ALLOW Decisions (Permitted)</div>
            <div class="metric-value" style="color: #10B981;">{metrics['allow_decisions']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #F59E0B;">
            <div class="metric-label">ASK CUSTOMER (Confirmation Required)</div>
            <div class="metric-value" style="color: #F59E0B;">{metrics['ask_customer_decisions']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #EF4444;">
            <div class="metric-label">BLOCK Decisions (Rejected)</div>
            <div class="metric-value" style="color: #EF4444;">{metrics['block_decisions']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Project Description & Purpose
    col_left, col_right = st.columns([1.2, 1])
    with col_left:
        st.markdown("### **Project Purpose & Executive Overview**")
        st.markdown("""
        The **Agent Gatekeeper** system addresses a critical emerging frontier in airline digital strategy: 
        the proliferation of autonomous consumer **AI agents** (such as personal travel assistants, auto-booking bots, 
        and conversational LLMs) operating on behalf of airline passengers.

        While AI agents offer unparalleled customer convenience—from finding cheap fares to auto-booking flights—they 
        introduce unprecedented enterprise risks around **unauthorized transactions**, **customer account compromise**, 
        **financial liability**, and **regulatory non-compliance**.

        Instead of an indiscriminate complete ban on AI agents, this prototype simulates a **Granular Permission and 
        Zero-Trust Gatekeeper** for **Delta Air Lines**:
        1. **Autonomous Registration & Consent:** Customers register authorized agents and assign scoped privileges.
        2. **Three-Tier Dynamic Decision Engine:** 
           - **`ALLOW`**: Low-risk read-only fare inquiries and pre-authorized micro-bookings (≤$100 demo limit).
           - **`ASK CUSTOMER`**: Higher-value bookings, itinerary modifications, and refunds require explicit human confirmation.
           - **`BLOCK`**: Unknown agents, revoked assistants, customer mismatches, and unauthorized requests are rejected immediately.
        3. **Revocation Guarantee:** Revoked agents are permanently barred from taking future actions.
        4. **Immutable Audit Trail:** Every event is recorded in a tamper-resistant JSON Lines format.
        """)

    with col_right:
        st.markdown("### **Business Rules Hierarchy**")
        st.markdown("""
        Decisions are evaluated against eight rules in strict hierarchical priority:

| Priority | Rule ID & Name | Scope / Trigger | Decision Outcome |
| :---: | :--- | :--- | :--- |
| **1st** | **R1 – Unknown Agent** | Agent not registered in system | **`BLOCK`** |
| **2nd** | **R2 – Revoked Agent** | Agent was revoked by customer | **`BLOCK`** |
| **3rd** | **R3 – Customer Mismatch** | Request customer ≠ registered owner | **`BLOCK`** |
| **4th** | **R8 – Unauthorized / Invalid** | Missing privilege, bad amount | **`BLOCK`** |
| **5th** | **R4 – View Fares** | Read-only fare search | **`ALLOW`** |
| **6th** | **R5 – Book Flight** | Amount ≤ $100 vs. > $100 | **`ALLOW`** / **`ASK`** |
| **7th** | **R6 – Change Flight** | Itinerary / seat modification | **`ASK CUSTOMER`** |
| **8th** | **R7 – Request Refund** | Ticket refund processing | **`ASK CUSTOMER`** |
        """)


# =============================================================================
# MODULE 2: REGISTER AI AGENT
# =============================================================================
elif nav_selection == "📝 Register AI Agent":
    st.subheader("Customer AI Agent Registration Portal")
    st.markdown("""
    Customers can register their authorized third-party or personal AI assistants (e.g., Siri, ChatGPT Travel Assistant, 
    Google Gemini Agent) and grant fine-grained permissions.
    """)

    with st.form("register_agent_form"):
        col1, col2 = st.columns(2)
        with col1:
            customer_id = st.text_input("Customer ID *", value="CUST001", help="Unique Delta SkyMiles or Customer Identifier")
            customer_name = st.text_input("Customer Full Name (Optional)", value="Veerparam Chauhan")
        with col2:
            agent_name = st.text_input("AI Agent Name *", placeholder="e.g. SkyBot, TravelMate, SiriAgent")
            st.info("ℹ️ A unique Agent ID (e.g. `DAL-AGT-XXXXXX`) will be automatically generated upon submission.")

        st.markdown("#### **Configure Agent Permissions**")
        st.caption("Select the specific airline operations this AI agent is authorized to perform on your behalf:")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            p_view = st.checkbox("🔍 View Flight Fares (Read-Only Search)", value=True)
            p_book = st.checkbox("💳 Book Flights (Autonomous up to $100 limit)", value=True)
        with p_col2:
            p_change = st.checkbox("🔄 Change Flights (Subject to confirmation)", value=True)
            p_refund = st.checkbox("💰 Request Refunds (Subject to confirmation)", value=False)

        submit_reg = st.form_submit_button("Register AI Agent", type="primary")

    if submit_reg:
        if not customer_id.strip():
            st.error("Please enter a valid Customer ID.")
        elif not agent_name.strip():
            st.error("Please enter an AI Agent Name.")
        else:
            perms = {
                "view_fares": p_view,
                "book_flights": p_book,
                "change_flights": p_change,
                "request_refunds": p_refund,
            }
            res = storage.register_agent(
                customer_id=customer_id,
                agent_name=agent_name,
                permissions=perms,
                customer_name=customer_name
            )

            if res["success"]:
                st.success(f"🎉 **Registration Successful!** {res['message']}")
                agent_info = res["agent"]
                st.json(agent_info)
            else:
                st.warning(f"⚠️ {res['error']}")

    st.markdown("---")
    st.markdown("### Currently Registered Agents")
    all_agents = storage.load_agents()
    if all_agents:
        df_agents = pd.DataFrame(all_agents)
        st.dataframe(df_agents[["agent_id", "agent_name", "customer_id", "status", "registered_at", "revoked_at"]], use_container_width=True)
    else:
        st.info("No agents currently registered.")


# =============================================================================
# MODULE 3: CHECK AI AGENT REQUEST
# =============================================================================
elif nav_selection == "🛡️ Check Agent Request":
    st.subheader("Simulate & Evaluate AI Agent Requests")
    st.markdown("""
    Evaluate incoming agent requests in real-time. The Gatekeeper verifies agent registration, active status, 
    customer identity, permissions, and policy limits before rendering a decision.
    """)

    all_agents = storage.load_agents()
    agent_options = [f"{a['agent_name']} ({a['agent_id']}) - Customer: {a['customer_id']} [{a['status']}]" for a in all_agents]
    agent_options.insert(0, "➕ Custom / Unknown Agent (Manual Entry)")

    col_select, col_empty = st.columns([2, 1])
    with col_select:
        selected_agent_choice = st.selectbox("Select Agent to Test:", agent_options)

    with st.form("check_request_form"):
        col1, col2 = st.columns(2)
        with col1:
            if selected_agent_choice == "➕ Custom / Unknown Agent (Manual Entry)":
                req_customer_id = st.text_input("Customer ID *", value="CUST001")
                req_agent_ident = st.text_input("Agent Name or ID *", value="UnknownBot")
            else:
                # Extract agent_id from selection
                chosen_idx = agent_options.index(selected_agent_choice) - 1
                chosen_agent = all_agents[chosen_idx]
                req_customer_id = st.text_input("Customer ID *", value=chosen_agent["customer_id"])
                req_agent_ident = st.text_input("Agent Name or ID *", value=chosen_agent["agent_name"])

        with col2:
            action_choice = st.selectbox(
                "Requested Action *",
                ["View flight fares", "Book flight", "Change flight", "Request refund"]
            )
            amount_val = 0.0
            if action_choice in ["Book flight", "Request refund"]:
                amount_val = st.number_input(
                    "Transaction Amount (USD) *",
                    min_value=0.0,
                    value=80.0 if action_choice == "Book flight" else 150.0,
                    step=10.0,
                    help="Demonstration threshold: ≤$100 is allowed; >$100 requires customer confirmation."
                )
            else:
                st.caption("ℹ️ Read-only and itinerary change requests do not require an upfront transaction amount.")
                amount_val = None

        evaluate_btn = st.form_submit_button("Evaluate Request", type="primary")

    if evaluate_btn:
        with st.spinner("Evaluating request against Gatekeeper business rules..."):
            result = gatekeeper.evaluate_request(
                customer_id=req_customer_id,
                agent_identifier=req_agent_ident,
                action=action_choice,
                amount=amount_val
            )

        dec = result["decision"]
        r_id = result["rule_id"]
        r_name = result["rule_name"]
        reason = result["reason"]
        exec_status = result["execution_status"]

        # Styled output box
        if dec == rules.ALLOW:
            box_cls = "decision-allow"
            pill_cls = "pill-allow"
            icon = "✅"
        elif dec == rules.ASK_CUSTOMER:
            box_cls = "decision-ask"
            pill_cls = "pill-ask"
            icon = "⚠️"
        else:
            box_cls = "decision-block"
            pill_cls = "pill-block"
            icon = "🛑"

        st.markdown(f"""
        <div class="decision-box {box_cls}">
            <div class="decision-header">
                <span>{icon} Decision: <b>{dec}</b></span>
            </div>
            <div style="margin-top: 8px; font-size: 15px;">
                <b>Applied Rule:</b> <span style="font-weight: 600; color: #002244;">{r_id} – {r_name}</span>
            </div>
            <div style="margin-top: 8px; font-size: 14px; color: #334155; line-height: 1.5;">
                <b>Reason:</b> {reason}
            </div>
            <div style="margin-top: 10px;">
                <span class="status-pill {pill_cls}">Execution Status: <b>{exec_status}</b></span>
                <span style="font-size: 12px; color: #64748B; margin-left: 10px;">Logged under Event ID: <code>{result['audit_event_id']}</code></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Explicit warning that ASK CUSTOMER does not execute
        if dec == rules.ASK_CUSTOMER:
            st.info("🔔 **Confirmation Pending:** The transaction has NOT been booked or executed. A push notification has been simulated for customer confirmation.")


# =============================================================================
# MODULE 4: REVOKE AI AGENT
# =============================================================================
elif nav_selection == "🚫 Revoke AI Agent":
    st.subheader("Revoke AI Agent Access & Maintain Proof of Revocation")
    st.markdown("""
    In accordance with regulatory trends (e.g. Wells Fargo revocation guidance), customers must be able to 
    unilaterally revoke an AI agent's access at any time. Revocation is permanent, recorded with an exact 
    ISO 8601 timestamp with timezone info, and preserved forever in the audit log.
    """)

    active_agents = [a for a in storage.load_agents() if a.get("status") == "ACTIVE"]

    if not active_agents:
        st.warning("No active agents available for revocation.")
    else:
        with st.form("revoke_agent_form"):
            agent_to_revoke_str = st.selectbox(
                "Select Active Agent to Revoke:",
                [f"{a['agent_name']} (ID: {a['agent_id']}) – Customer: {a['customer_id']}" for a in active_agents]
            )
            revoked_by_role = st.text_input("Revocation Requested By:", value="Customer (via Delta Web Portal)")
            confirm_check = st.checkbox("I confirm that I wish to permanently revoke all access permissions for this AI agent.")

            revoke_btn = st.form_submit_button("Permanently Revoke Agent Access", type="primary")

        if revoke_btn:
            if not confirm_check:
                st.error("Please check the confirmation box before proceeding.")
            else:
                idx = [f"{a['agent_name']} (ID: {a['agent_id']}) – Customer: {a['customer_id']}" for a in active_agents].index(agent_to_revoke_str)
                target = active_agents[idx]

                res = storage.revoke_agent(
                    agent_id=target["agent_id"],
                    revoked_by=revoked_by_role
                )

                if res["success"]:
                    st.success(f"🛑 **Agent Revoked Successfully!**")
                    st.markdown(f"""
                    **Revocation Certificate:**
                    - **Agent Name:** `{target['agent_name']}`
                    - **Agent ID:** `{target['agent_id']}`
                    - **Customer ID:** `{target['customer_id']}`
                    - **Revocation Timestamp (ISO 8601):** `{res['revoked_at']}`
                    - **Revocation Authority:** `{revoked_by_role}`
                    - **Future Requests:** All future requests from this agent will be **`BLOCKED`** under Rule **R2**.
                    """)
                else:
                    st.error(res["error"])

    st.markdown("---")
    st.markdown("### Agent Status Overview")
    all_agents = storage.load_agents()
    if all_agents:
        st.dataframe(pd.DataFrame(all_agents)[["agent_id", "agent_name", "customer_id", "status", "registered_at", "revoked_at", "revoked_by"]], use_container_width=True)


# =============================================================================
# MODULE 5: IMMUTABLE AUDIT TRAIL
# =============================================================================
elif nav_selection == "📜 Immutable Audit Trail":
    st.subheader("Immutable Audit Log & Compliance Trail")
    st.markdown("""
    Every registration, evaluation, and revocation event is permanently recorded in **JSON Lines (`audit_log.jsonl`)**.
    Historical records are never overwritten and persist across application restarts.
    """)

    df_logs = storage.get_audit_dataframe()

    if df_logs.empty:
        st.info("No audit logs recorded yet.")
    else:
        # Search & Filter Controls
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            filter_decision = st.multiselect("Filter by Decision:", options=df_logs["decision"].unique().tolist(), default=[])
        with col_f2:
            filter_action = st.multiselect("Filter by Action:", options=df_logs["action"].unique().tolist(), default=[])
        with col_f3:
            filter_event = st.multiselect("Filter by Event Type:", options=df_logs["event_type"].unique().tolist(), default=[])
        with col_f4:
            search_term = st.text_input("Search (Customer / Agent / Reason):", placeholder="e.g. CUST001, TravelBot...")

        # Apply Filters
        filtered_df = df_logs.copy()
        if filter_decision:
            filtered_df = filtered_df[filtered_df["decision"].isin(filter_decision)]
        if filter_action:
            filtered_df = filtered_df[filtered_df["action"].isin(filter_action)]
        if filter_event:
            filtered_df = filtered_df[filtered_df["event_type"].isin(filter_event)]
        if search_term.strip():
            term = search_term.strip().lower()
            filtered_df = filtered_df[
                filtered_df["customer_id"].astype(str).str.lower().str.contains(term) |
                filtered_df["agent_id"].astype(str).str.lower().str.contains(term) |
                filtered_df["agent_name"].astype(str).str.lower().str.contains(term) |
                filtered_df["reason"].astype(str).str.lower().str.contains(term)
            ]

        st.caption(f"Showing **{len(filtered_df)}** of **{len(df_logs)}** audit events (Newest records shown top).")

        # Display descending (latest first)
        display_df = filtered_df.iloc[::-1].reset_index(drop=True)
        st.dataframe(
            display_df[[
                "event_id", "timestamp", "event_type", "customer_id",
                "agent_name", "action", "amount", "decision", "rule_id",
                "reason", "agent_status"
            ]],
            use_container_width=True
        )

        # CSV Download
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Audit Log as CSV",
            data=csv_data,
            file_name=f"delta_gatekeeper_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


# =============================================================================
# MODULE 6: AUTOMATED TEST RUNNER
# =============================================================================
elif nav_selection == "🧪 Automated Test Runner":
    st.subheader("Automated Test Suite & Verification Results")
    st.markdown("""
    Run the automated test suite directly to verify all 7 core assignment test cases. 
    Tests execute in an isolated sandbox with mock data files, ensuring live database records remain untouched.
    """)

    if st.button("🚀 Run All 7 Automated Tests Now", type="primary"):
        from tests.test_gatekeeper import run_all_tests_with_summary_table
        with st.spinner("Executing automated test suite..."):
            test_results = run_all_tests_with_summary_table()
        
        st.success("✅ Test suite execution complete!")
        df_res = pd.DataFrame(test_results)
        
        # Display formatted table
        st.dataframe(
            df_res[["test_num", "scenario", "expected_decision", "actual_decision", "expected_rule", "actual_rule", "status"]],
            use_container_width=True
        )
    else:
        st.info("Click the button above to run the automated test suite and generate genuine test results.")


# =============================================================================
# MODULE 7: ACADEMIC CONTEXT & SOURCES
# =============================================================================
elif nav_selection == "📚 Academic Context & Sources":
    st.subheader("Academic Context, Industry Sources & References")

    st.markdown("""
    ### **Industry Context: The Rise of Autonomous Customer AI Agents**

    #### 1. Wells Fargo – AI Revocation Mandates
    - **Context:** Wells Fargo updated customer account terms to clarify liability regarding AI agents operating on customer accounts. 
      The bank established guidelines requiring customers to be capable of revoking third-party agent access and maintaining documented proof.
    - **Citation:** American Banker (2024), *Wells Fargo wants customers to prove they've revoked AI agents*.  
      URL: [American Banker Article](https://www.americanbanker.com/news/wells-fargo-wants-customers-to-prove-theyve-revoked-ai-agents)

    #### 2. JPMorgan Chase – AI Agent Restrictions
    - **Context:** JPMorgan Chase restricted automated external AI agents from acting on behalf of retail customers due to security, 
      unauthorized trading, and identity spoofing concerns.
    - **Citation:** Reported in industry coverage on retail financial services security and autonomous consumer agents.

    #### 3. Delta Air Lines & Travel Sector Evaluation
    - **Context:** Travel sector and tech industry coverage highlighted that major consumer enterprises, including Delta Air Lines, 
      Amazon, and Schwab, are evaluating approaches to third-party AI agents attempting automated bookings and ticket changes.
    - **Citation:** OfficeChai (2024), *Amazon, JPMorgan, Schwab, and Delta are all blocking AI agents: Here's why*.  
      URL: [OfficeChai Article](https://officechai.com/ai/amazon-jpmorgan-schwab-and-delta-are-all-blocking-ai-agents-heres-why/)

    #### 4. Additional Academic & Technical Standards Source
    - **National Institute of Standards and Technology (NIST):**  
      *Artificial Intelligence Risk Management Framework (NIST AI RMF 1.0)*, NIST Special Publication 1270, 2023.  
      Recommends governance and boundary control mechanisms for autonomous AI actors, emphasizing identity validation, 
      delegated authority scoping, and human-in-the-loop safeguards.
    - **OWASP Top 10 for Large Language Model Applications (2025):**  
      *LLM06: Excessive Agency*, emphasizing that autonomous agents must not be granted unchecked privileges to execute 
      financial transactions without explicit customer validation and strict permission checks.

    ---
    ### **Academic Prototype Disclaimer**
    *This software prototype, its rule set (R1–R8), and the USD 100 booking demonstration threshold are created solely for academic evaluation 
    by Veerparam Chauhan (PGD202563340). It is not affiliated with, officially sponsored by, or endorsed by Delta Air Lines, Inc.*
    """)
