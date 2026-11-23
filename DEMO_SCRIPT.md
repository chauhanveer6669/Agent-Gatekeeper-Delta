# 2-Minute Video Demonstration Script & Recording Guide

**Student Name:** Veerparam Chauhan  
**Enrolment Number:** PGD202563340  
**Selected Industry:** Airline | **Company:** Delta Air Lines  
**Project Title:** Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines  
**Target Video Duration:** Maximum 2 Minutes (120 Seconds)  

---

## 1. How to Record on Your Mac (Step-by-Step)

1. **Launch the Application First:**
   Open Terminal and run:
   ```bash
   cd /Users/veerugujjar/.gemini/antigravity/scratch/Agent-Gatekeeper-Delta
   streamlit run app.py
   ```
   Open your browser to `http://localhost:8501` and maximize the window.

2. **Start Screen Recording:**
   - Press **`Cmd + Shift + 5`** on your Mac keyboard.
   - Select **Record Entire Screen** or **Record Selected Portion** (drag over your browser window).
   - Under **Options**, ensure your **Microphone** is turned ON so your voice is recorded clearly.
   - Click **Record**.

3. **Follow the Exact Script Below:** Speak at a steady, professional pace. Keep an eye on your timer.

---

## 2. Timed Demonstration Script (Exactly 120 Seconds)

### [0:00 – 0:20] Segment 1: Introduction & Problem Context (20 seconds)
- **On Screen:** Dashboard header showing: *Student: Veerparam Chauhan | Enrolment No: PGD202563340 | Delta Air Lines*.
- **Speak:**  
  > *"Hello Professor. My name is Veerparam Chauhan, enrolment number PGD202563340. Today I am presenting my individual MBA project: **Agent Gatekeeper** for **Delta Air Lines**.*  
  > *As passengers adopt autonomous consumer AI agents to search and book travel, airlines face a dilemma: completely blocking agents degrades customer convenience, while unrestricted access risks unauthorized bookings and liability.*  
  > *Our system provides a zero-trust policy gatekeeper that evaluates agent actions in real time."*

---

### [0:20 – 0:45] Segment 2: Dashboard Overview & Priority Rules (25 seconds)
- **On Screen:** Point to the KPI metric cards (Total Agents, Active, Revoked, ALLOW, ASK CUSTOMER, BLOCK counts) and the rules hierarchy.
- **Speak:**  
  > *"On the dashboard, we monitor registered agents and decision metrics. Incoming requests are evaluated through eight sequential business rules in strict priority: unknown agents are blocked under R1, revoked agents under R2, and identity mismatches under R3.*  
  > *Low-risk searches are allowed under R4, while financial actions follow tiered limits."*

---

### [0:45 – 1:15] Segment 3: Live Request Evaluation – ALLOW vs. ASK CUSTOMER (30 seconds)
- **On Screen:** Navigate to **"🛡️ Check Agent Request"** in the sidebar.
  1. Select `TravelBot`, choose `Book flight`, set Amount to **$80**, click **Evaluate Request**. (Green **ALLOW** banner appears).
  2. Change Amount to **$250**, click **Evaluate Request**. (Amber **ASK CUSTOMER** banner appears).
- **Speak:**  
  > *"Let's test an active agent, TravelBot. First, a booking of $80 is evaluated: the Gatekeeper returns **ALLOW** under Rule R5 because it is within the $100 demonstration threshold.*  
  > *Now, if TravelBot requests a $250 booking, the Gatekeeper returns **ASK CUSTOMER**. Crucially, the transaction is **not executed automatically**; it pauses safely in a pending confirmation state with a simulated out-of-band notification."*

---

### [1:15 – 1:40] Segment 4: Irrevocable Revocation & Enforcement (25 seconds)
- **On Screen:** Navigate to **"🚫 Revoke AI Agent"** in sidebar.
  1. Select `TravelBot`, check confirmation, and click **Permanently Revoke Agent Access**. (Revocation certificate with timestamp appears).
  2. Return to **"🛡️ Check Agent Request"** and submit any request for `TravelBot`. (Red **BLOCK** banner appears under **R2**).
- **Speak:**  
  > *"Following regulatory guidance like Wells Fargo's revocation mandates, passengers must be able to revoke agents at any time. Here, the customer revokes TravelBot, generating an immutable ISO 8601 timestamped receipt.*  
  > *When we immediately test another request from TravelBot, it is permanently **BLOCKED** under Rule R2, regardless of its prior permissions."*

---

### [1:40 – 2:00] Segment 5: Immutable Audit Trail & Conclusion (20 seconds)
- **On Screen:** Navigate to **"📜 Immutable Audit Trail"** in sidebar. Point to the table and click **"📥 Download Audit Log as CSV"**.
- **Speak:**  
  > *"Every event—registration, evaluation, and revocation—is permanently appended to a tamper-resistant JSON Lines audit log and can be exported to CSV for regulatory compliance.*  
  > *In conclusion, Delta Air Lines should implement this controlled gatekeeper architecture to balance consumer AI convenience with robust enterprise security. Thank you."*

---

## 3. Post-Recording Checklist

- [ ] Check video length: Ensure it is **between 1:45 and 2:00 minutes** (must not exceed 2:00).
- [ ] Check audio quality: Verify that your voice is audible and clear.
- [ ] Check video resolution: Verify text on screen is legible (1080p recommended).
- [ ] Save the video file as: `PGD202563340_Demo_Video.mp4` (or upload to YouTube/Vimeo/Google Drive as an unlisted link if your portal requires a URL).
