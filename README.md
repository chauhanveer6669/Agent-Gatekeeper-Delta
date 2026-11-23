# Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines

> **MBA Individual Assignment**  
> **Student Name:** Veerparam Chauhan  
> **Enrolment Number:** PGD202563340  
> **Selected Industry:** Airline  
> **Selected Company:** Delta Air Lines  
> **Academic Prototype Notice:** *This system is an academic simulation and educational prototype. It is not officially developed, approved, or sponsored by Delta Air Lines, Inc.*

---

## 1. Executive Summary & Purpose

The **Agent Gatekeeper** is a zero-trust permission and policy enforcement engine designed for the aviation sector. As consumers increasingly adopt autonomous Artificial Intelligence (AI) agents—such as digital travel concierges, personal LLMs, and autonomous price-monitoring bots—they delegate high-consequence travel operations to software actors acting on their behalf.

These agents can search fares, book tickets, change flight itineraries, and request refunds. Without rigorous controls, airlines face significant enterprise risks, including unauthorized credit card commitments, account takeover, non-refundable ticket cancellations, and regulatory non-compliance.

The **Agent Gatekeeper** provides a robust, policy-driven control layer that evaluates incoming agent requests against eight sequential business rules, rendering one of three decisions:
1. **`ALLOW`**: Automatically permits low-risk, pre-authorized actions (e.g. read-only fare search or autonomous bookings under the \$100 demonstration threshold).
2. **`ASK CUSTOMER`**: Mandatory human-in-the-loop safeguard for high-stakes operations (bookings over \$100, ticket changes, refunds). **The transaction is NOT executed automatically**; it pauses safely until explicit customer verification is confirmed.
3. **`BLOCK`**: Instantly terminates unauthorized, unregistered, mismatched, or revoked agent requests.

Additionally, the system provides self-service agent registration, unilateral and irreversible customer revocation with ISO 8601 timestamped proof, and an immutable JSON Lines audit log.

---

## 2. Core Business Rules Architecture

All requests are evaluated in strict priority order (R1 → R2 → R3 → R8 → R4 → R5 → R6 → R7):

| Priority | Rule ID | Rule Name | Description & Demonstration Threshold | Decision | Execution Status |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **1st** | **R1** | Unknown Agent | Unregistered AI agent attempts an action. | **`BLOCK`** | Blocked / Not executed |
| **2nd** | **R2** | Revoked Agent | Customer previously revoked the agent; all future requests are barred. | **`BLOCK`** | Blocked / Not executed |
| **3rd** | **R3** | Customer Identity Mismatch | Request Customer ID ≠ Registered Agent Owner ID. | **`BLOCK`** | Blocked / Not executed |
| **4th** | **R8** | Invalid or Unauthorized Request | Missing required permissions, negative amount, or bad action. | **`BLOCK`** | Blocked / Not executed |
| **5th** | **R4** | View Flight Fares | Registered, active agent with `view_fares` permission (read-only). | **`ALLOW`** | Executed |
| **6th** | **R5** | Book Flights | Booking ≤ \$100: ALLOW  \|  Booking > \$100: ASK CUSTOMER. | **`ALLOW`** / **`ASK`** | Executed / Waiting for Confirmation |
| **7th** | **R6** | Change Flights | Changing existing flight booking requires human confirmation. | **`ASK CUSTOMER`** | Waiting for Confirmation |
| **8th** | **R7** | Request Refund | Refund requires confirmation & compliance with fare rules. | **`ASK CUSTOMER`** | Waiting for Confirmation |

*Note on Demonstration Threshold:* The USD 100 booking limit is an academic simulation threshold for testing autonomous limits, not an actual Delta Air Lines policy.

---

## 3. Technology Stack

- **Programming Language:** Python 3 (beginner-friendly, clean modular architecture)
- **User Interface:** Streamlit (interactive web dashboard with Delta Navy `#002244` and Red `#E01933` branding)
- **Agent Registration Storage:** JSON (`data/agents.json`) for persistent agent profiles and permissions
- **Audit Logging:** JSON Lines (`data/audit_log.jsonl`) for immutable, append-only compliance logs
- **Data Analysis & Export:** Pandas for filtering, tabular visualization, and CSV export
- **Automated Testing:** Pytest for isolated, reproducible automated test suite execution
- **Academic Report Generation:** Matplotlib PDF backend (`report/AgentGatekeeper_Report.pdf`) strictly limited to 2 pages

---

## 4. Project Directory Structure

```
Agent-Gatekeeper-Delta/
├── app.py                      # Main Streamlit web application & UI dashboard
├── gatekeeper.py               # Core orchestrator evaluating requests & coordinating audit logs
├── rules.py                    # Independent business rules engine implementing R1 through R8
├── storage.py                  # Persistent JSON storage, JSONL audit logs, and metrics
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive project documentation and terminal commands
├── PROMPTS.md                  # Development prompt documentation & student contribution log
├── .gitignore                  # Git exclusions for clean repository tracking
├── data/
│   ├── agents.json             # Persistent agent registrations & permissions
│   └── audit_log.jsonl         # Immutable append-only audit event trail
├── tests/
│   └── test_gatekeeper.py      # Pytest automated test suite (all 7 core test cases + edge cases)
├── report/
│   ├── report.md               # Full academic report in Markdown format
│   ├── generate_report.py      # Automated script generating the 2-page PDF report
│   └── AgentGatekeeper_Report.pdf # Verified 2-page academic submission PDF
└── screenshots/
    ├── report_page_1.png       # High-resolution preview of Report Page 1
    └── report_page_2.png       # High-resolution preview of Report Page 2
```

---

## 5. Step-by-Step Installation & Setup (Mac Terminal)

Open your **Terminal** application on macOS and follow these simple steps:

### Step 1: Navigate to the Project Directory
```bash
cd /Users/veerugujjar/.gemini/antigravity/scratch/Agent-Gatekeeper-Delta
```

### Step 2: (Optional but Recommended) Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. How to Run the Application

Launch the Streamlit interactive dashboard with:

```bash
streamlit run app.py
```

Streamlit will launch automatically in your default web browser at:
`http://localhost:8501`

### Exploring Application Features:
1. **📊 Dashboard & Overview:** Review high-level metrics (Total Agents, Active, Revoked, Total Requests, ALLOW/ASK/BLOCK counts), business problem context, and the rules priority matrix.
2. **📝 Register AI Agent:** Enter a Customer ID (e.g. `CUST001`), an Agent Name (e.g. `SkyBot`), and toggle specific permissions (`view_fares`, `book_flights`, `change_flights`, `request_refunds`). Click **Register AI Agent** to persist to `data/agents.json`.
3. **🛡️ Check Agent Request:** Select an existing registered agent or enter custom parameters. Choose an action (e.g. Book Flight for \$80 vs \$250) and view the instant decision banner (`ALLOW`, `ASK CUSTOMER`, or `BLOCK`), applied rule ID, and plain-English justification.
4. **🚫 Revoke AI Agent:** Select an active agent, enter the revocation authority (e.g. `Customer (via Delta Web Portal)`), and confirm revocation. A certificate with an ISO 8601 timestamp is generated, and all future requests are permanently blocked.
5. **📜 Immutable Audit Trail:** Search and filter historical events by decision, action, or keyword, and download the full audit log as a CSV spreadsheet.
6. **🧪 Automated Test Runner:** Click the verification button inside the web app to execute all 7 tests live and display the genuine verification table.

---

## 7. How to Run Automated Tests

To run the automated tests and verify all 7 core assignment scenarios:

### Option A: Standalone Runner (Prints Formatted Summary Table)
```bash
python3 tests/test_gatekeeper.py
```

### Option B: Pytest Test Runner (Verbose Output)
```bash
pytest tests/test_gatekeeper.py -v
```

### Genuine Test Results Summary Table:
| Test # | Test Scenario | Customer ID | Agent Name | Action & Amount | Expected Decision | Actual Decision | Expected Rule | Actual Rule | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TEST 1** | Known Active Agent, View Fares | CUST001 | TravelBot | View flight fares | ALLOW | ALLOW | R4 | R4 | **PASS** |
| **TEST 2** | Unknown Agent | CUST001 | UnknownBot | Book flight (\$50) | BLOCK | BLOCK | R1 | R1 | **PASS** |
| **TEST 3** | Booking Above Limit | CUST001 | TravelBot | Book flight (\$250) | ASK CUSTOMER | ASK CUSTOMER | R5 | R5 | **PASS** |
| **TEST 4** | Booking Below Limit | CUST001 | TravelBot | Book flight (\$80) | ALLOW | ALLOW | R5 | R5 | **PASS** |
| **TEST 5** | Revoked Agent Booking Attempt | CUST001 | TravelBot | Book flight (\$50) | BLOCK | BLOCK | R2 | R2 | **PASS** |
| **TEST 6** | Change Flight Request | CUST001 | TravelBot | Change flight | ASK CUSTOMER | ASK CUSTOMER | R6 | R6 | **PASS** |
| **TEST 7** | Refund Request | CUST001 | TravelBot | Request refund | ASK CUSTOMER | ASK CUSTOMER | R7 | R7 | **PASS** |

*All 7 core test cases and 3 supplementary edge-case tests pass 100% in isolated temporary storage without touching production data.*

---

## 8. How to Regenerate the 2-Page Academic Report PDF

To recompile the official two-page academic report:

```bash
python3 report/generate_report.py
```
This generates `report/AgentGatekeeper_Report.pdf` and saves high-resolution visual previews in `screenshots/`.

---

## 9. Git Repository & Multi-Day Commit Strategy

### Genuine Multi-Day Commit Plan (5+ Commits Across 3+ Days)
To satisfy the MBA assignment requirement of at least 5 genuine commits spread across at least 3 distinct calendar days without faking Git history, follow this suggested progression:

#### **Day 1: Project Foundation & Core Rules**
- Initialize repository and configure `.gitignore`.
- Implement `rules.py` with all 8 business rules and priority order.
- Commit 1: `git commit -m "feat: initialize project structure and implement business rules R1-R8"`
- Implement `storage.py` (JSON registration and JSONL immutable audit logging).
- Commit 2: `git commit -m "feat: implement persistent storage layer for agents and audit logs"`

#### **Day 2: Gatekeeper Engine & Automated Testing**
- Implement `gatekeeper.py` request orchestration and decision tracking.
- Commit 3: `git commit -m "feat: implement core gatekeeper decision engine and audit integration"`
- Implement `tests/test_gatekeeper.py` with pytest fixtures and test cases 1–7.
- Commit 4: `git commit -m "test: implement automated test suite with isolated fixtures for tests 1-7"`

#### **Day 3: Streamlit Interface, Academic Report & Polish**
- Implement `app.py` Streamlit UI with Delta Air Lines styling and dashboard metrics.
- Commit 5: `git commit -m "feat: build interactive Streamlit dashboard with Delta styling"`
- Generate 2-page academic PDF report, README, and documentation.
- Commit 6: `git commit -m "docs: compile 2-page academic report, PROMPTS log, and documentation"`

### Exact Terminal Commands to Initialize and Push to GitHub:

```bash
# 1. Initialize local Git repository
cd /Users/veerugujjar/.gemini/antigravity/scratch/Agent-Gatekeeper-Delta
git init

# 2. Add files and make initial commit
git add .
git commit -m "feat: initialize Agent Gatekeeper project for Delta Air Lines"

# 3. Add remote GitHub repository (after creating an empty repo on GitHub)
git remote add origin https://github.com/VeerparamChauhan/Agent-Gatekeeper-Delta.git

# 4. Rename default branch to main and push
git branch -M main
git push -u origin main
```

---

## 10. Academic Integrity & Industry Sources

1. **American Banker (2024):** *Wells Fargo wants customers to prove they've revoked AI agents*.  
   URL: https://www.americanbanker.com/news/wells-fargo-wants-customers-to-prove-theyve-revoked-ai-agents
2. **OfficeChai (2024):** *Amazon, JPMorgan, Schwab, and Delta are all blocking AI agents: Here's why*.  
   URL: https://officechai.com/ai/amazon-jpmorgan-schwab-and-delta-are-all-blocking-ai-agents-heres-why/
3. **NIST (2023):** *Artificial Intelligence Risk Management Framework (NIST AI RMF 1.0)*, NIST SP 1270, U.S. Department of Commerce.
4. **OWASP (2025):** *OWASP Top 10 for Large Language Model Applications – LLM06: Excessive Agency*.

---
*Created by Veerparam Chauhan (PGD202563340) for MBA Individual Assignment.*
