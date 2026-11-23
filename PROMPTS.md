# Project Prompt History & Development Log

**Course:** MBA Individual Assignment  
**Student Name:** Veerparam Chauhan  
**Enrolment Number:** PGD202563340  
**Project Title:** Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines  
**Selected Industry:** Airline | **Selected Company:** Delta Air Lines  

---

## 1. Master Development Prompt

The following master prompt was used to initiate and guide the end-to-end development of the **Agent Gatekeeper** application:

```text
# MASTER PROJECT PROMPT – AGENT GATEKEEPER

Act as a senior Python developer, UI/UX designer, software tester, business analyst, and academic project guide.

I am an MBA student. I need to complete my individual assignment titled Agent Gatekeeper using Google Antigravity.

Your task is to BUILD a complete, working, professional, beginner-friendly project that satisfies every assignment requirement below.

Do not just explain what I should do. Create the actual project files, write the code, run the application, test it, fix errors, and prepare the academic report and submission folder.

## 1. STUDENT AND PROJECT DETAILS
Student Name: Veerparam Chauhan  
Enrolment Number: PGD202563340  
Selected Industry: Airline  
Selected Company: Delta Air Lines  

Project Title:
Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines

Display the student name, enrolment number, company name, and project title clearly on the application's dashboard and in the report.
Important: This is an academic prototype and simulation. Do not claim that it is officially developed, approved, or connected to Delta Air Lines.

## 2. UNDERSTAND THE BUSINESS PROBLEM
The project concerns the growing use of AI agents that perform activities on behalf of customers.
For example, a customer's AI agent might:
- Search and compare airline fares.
- Book flight tickets.
- Change existing bookings.
- Request refunds.
- Access customer information.

The company must decide whether to:
1. ALLOW – permit the request.
2. ASK CUSTOMER – require customer confirmation before proceeding.
3. BLOCK – reject the request.

The system must also allow customers to register an AI agent, define its permissions, revoke its access, and maintain a permanent audit record.

Use the following case background as context:
1. Wells Fargo introduced requirements for customers to revoke AI-agent access and retain proof of revocation.
Source: https://www.americanbanker.com/news/wells-fargo-wants-customers-to-prove-theyve-revoked-ai-agents
2. JPMorgan has restricted outside AI agents from acting for retail customers because of security, control, and liability concerns.
3. Delta Air Lines was reported to be evaluating its approach to third-party AI agents for airline transactions.
Source: https://officechai.com/ai/amazon-jpmorgan-schwab-and-delta-are-all-blocking-ai-agents-heres-why/

## 3. BUSINESS RULES – IMPLEMENT ALL EIGHT
Create a separate rules.py file and implement these eight rules:
R1 – UNKNOWN AGENT
R2 – REVOKED AGENT
R3 – CUSTOMER IDENTITY MISMATCH
R4 – VIEW FLIGHT FARES
R5 – BOOK FLIGHTS (USD 100 demonstration limit)
R6 – CHANGE FLIGHTS (ASK CUSTOMER)
R7 – REQUEST REFUND (ASK CUSTOMER)
R8 – INVALID OR UNAUTHORIZED REQUEST

Decision priority:
1. R1, 2. R2, 3. R3, 4. R8, 5. R4, 6. R5, 7. R6, 8. R7.

## 4. TECHNOLOGY REQUIREMENTS
Python, Streamlit, JSON (agents.json), JSON Lines (audit_log.jsonl), Pandas, Pytest.
Delta Air Lines navy-blue, white, and light-grey theme. Run locally on Mac.

## 5. APPLICATION FEATURES
A. Dashboard, B. Register AI Agent, C. Check AI Agent Request, D. Revoke AI Agent, E. Audit Log.

## 6. AUTOMATED TESTING
tests/test_gatekeeper.py with 7 required test cases.

## 7. PROJECT FOLDER STRUCTURE
Agent-Gatekeeper-Delta/ (app.py, gatekeeper.py, rules.py, storage.py, data/, tests/, report/, screenshots/).

## 8. ACADEMIC REPORT – MAXIMUM TWO PAGES
Professional academic report in PDF format (AgentGatekeeper_Report.pdf) with 12 required sections.
```

---

## 2. Interactive Development & Refinement Prompts

*This section documents subsequent follow-up prompts and interactions utilized during the implementation, testing, and verification phases:*

1. **Environment Setup & Verification:**
   - Prompt: *"Verify local Python 3 environment, installed packages (Streamlit, Pandas, Pytest, Matplotlib), and create project directory structure under scratch."*
2. **Business Rules & Storage Layer:**
   - Prompt: *"Implement rules.py enforcing strict priority evaluation R1 through R8, and storage.py with atomic JSON agent registrations and immutable JSON Lines audit logging."*
3. **Core Gatekeeper & Automated Pytest Suite:**
   - Prompt: *"Create gatekeeper.py orchestrator and tests/test_gatekeeper.py implementing isolated temp_path fixtures for all 7 required test cases and 3 supplementary tests."*
4. **Streamlit UI & Visual Dashboard:**
   - Prompt: *"Develop app.py with Delta Air Lines professional palette (Navy #002244, Red #E01933), metric KPI cards, self-service registration, evaluation simulator, revocation with timestamped certificates, and CSV export."*
5. **Academic Report PDF Compilation:**
   - Prompt: *"Generate a strictly two-page academic report in PDF format (report/AgentGatekeeper_Report.pdf) including all 12 required academic sections, test results table, and verified citations."*

---

## 3. Student Personal Contribution & Verification Log

> **Notice for Student (Veerparam Chauhan):**  
> *In accordance with academic integrity guidelines, the section below is provided for you to record the specific checks and personal modifications you performed on this project. Fill this in prior to your final assignment submission.*

### A. Feature or Code Section I Personally Checked
- **Component / File Checked:** `rules.py` (Rule R5 and Decision Priority Order)
- **Observations / Verification Notes:**  
  *[Student to add: e.g., "I personally examined lines 145-180 in rules.py to verify that booking amounts at or below USD 100 return ALLOW, while amounts above USD 100 trigger ASK CUSTOMER. I confirmed that the priority logic ensures revoked agents (R2) are evaluated before booking amounts (R5)."]*
- **Date Checked:** `[Enter Date, e.g. November 2026]`

### B. Change or Enhancement I Personally Made or Verified
- **Component / File Modified:** `tests/test_gatekeeper.py` / `app.py`
- **Specific Change Made or Verified:**  
  *[Student to add: e.g., "I personally executed pytest tests/test_gatekeeper.py in terminal and verified that all 10 tests passed. I also tested the revocation workflow in the Streamlit UI to confirm that revoking TravelBot immediately causes subsequent booking requests to be blocked under R2."]*
- **Date Verified:** `[Enter Date, e.g. November 2026]`

### C. Personal Reflection on Academic Findings
- **Reflection:**  
  *[Student to add: e.g., "Reviewing the case studies of Wells Fargo and JPMorgan highlighted that unrestricted AI access creates unacceptable financial liability. However, completely blocking AI agents hurts customer convenience. The Gatekeeper's tiered model provides the optimal balance for Delta Air Lines."]*
