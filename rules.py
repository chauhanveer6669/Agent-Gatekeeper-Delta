"""
Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines
Student: Veerparam Chauhan | Enrolment Number: PGD202563340
Industry: Airline | Company: Delta Air  Lines

Module: rules.py
Purpose: Defines and evaluates the 8 business rules governing AI Agent requests.

Important: This is an academic prototype and simulation.
The rules, thresholds (e.g., USD 100 booking limit), and decision logic are proposed
for this academic study and do not represent official Delta Air Lines policies.
"""

from typing import Dict, Any, Optional

# Decision Constants
ALLOW = "ALLOW"
ASK_CUSTOMER = "ASK CUSTOMER"
BLOCK = "BLOCK"

# Execution Status Constants
STATUS_EXECUTED = "Executed"
STATUS_WAITING_CONFIRMATION = "Waiting for customer confirmation (Not executed)"
STATUS_BLOCKED = "Blocked / Not executed"

# Canonical Action Mapping
ACTION_MAP = {
    "view_flight_fares": "View flight fares",
    "view_fares": "View flight fares",
    "view flight fares": "View flight fares",
    "view fares": "View flight fares",
    "book_flight": "Book flight",
    "book flight": "Book flight",
    "book flights": "Book flight",
    "change_flight": "Change flight",
    "change flight": "Change flight",
    "change flights": "Change flight",
    "request_refund": "Request refund",
    "request refund": "Request refund",
    "request refunds": "Request refund",
    "refund": "Request refund",
}

# Required Permission Mapping for Each Action
REQUIRED_PERMISSIONS = {
    "View flight fares": "view_fares",
    "Book flight": "book_flights",
    "Change flight": "change_flights",
    "Request refund": "request_refunds",
}

# Demonstration threshold for autonomous booking
BOOKING_DEMO_THRESHOLD_USD = 100.0


def normalize_action(action: str) -> Optional[str]:
    """
    Normalizes user or API action string to canonical representation.
    Returns None if action is unsupported.
    """
    if not action or not isinstance(action, str):
        return None
    cleaned = action.strip().lower().replace("-", "_")
    return ACTION_MAP.get(cleaned) or ACTION_MAP.get(action.strip())


def evaluate_rules(
    agent: Optional[Dict[str, Any]],
    customer_id: str,
    action: str,
    amount: Optional[float] = None
) -> Dict[str, Any]:
    """
    Evaluates an incoming AI agent request against all 8 business rules in strict priority order.

    Priority Order:
    1. R1 – Unknown agent
    2. R2 – Revoked agent
    3. R3 – Customer ID mismatch
    4. R8 – Invalid request or missing authorization
    5. R4 – View fares
    6. R5 – Book flights
    7. R6 – Change flights
    8. R7 – Refund

    Returns a dictionary containing:
    - decision: "ALLOW" | "ASK CUSTOMER" | "BLOCK"
    - rule_id: e.g. "R1", "R2", ...
    - rule_name: e.g. "Unknown Agent"
    - reason: Human-readable explanation
    - execution_status: "Executed" | "Waiting for customer confirmation" | "Blocked / Not executed"
    - normalized_action: Canonical action string or original
    - amount: Processed transaction amount
    """
    canonical_action = normalize_action(action)
    clean_cust_id = str(customer_id).strip() if customer_id else ""

    # -------------------------------------------------------------
    # PRIORITY 1: R1 – UNKNOWN AGENT
    # -------------------------------------------------------------
    if agent is None:
        return {
            "decision": BLOCK,
            "rule_id": "R1",
            "rule_name": "Unknown Agent",
            "reason": (
                "The AI agent is not registered in the system. Unregistered or unrecognized "
                "agents are blocked from accessing customer accounts or airline services."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": canonical_action or str(action),
            "amount": amount,
        }

    agent_name = agent.get("agent_name", "Unknown Agent")
    agent_id = agent.get("agent_id", "Unknown ID")
    agent_status = str(agent.get("status", "")).upper()
    registered_customer = str(agent.get("customer_id", "")).strip()
    agent_permissions = agent.get("permissions", {}) or {}

    # -------------------------------------------------------------
    # PRIORITY 2: R2 – REVOKED AGENT
    # -------------------------------------------------------------
    if agent_status == "REVOKED":
        revoked_at = agent.get("revoked_at", "an earlier recorded time")
        return {
            "decision": BLOCK,
            "rule_id": "R2",
            "rule_name": "Revoked Agent",
            "reason": (
                f"The AI agent '{agent_name}' ({agent_id}) was revoked by the customer on {revoked_at}. "
                "Every future request from a revoked agent is permanently blocked, regardless "
                "of previously granted permissions."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": canonical_action or str(action),
            "amount": amount,
        }

    # -------------------------------------------------------------
    # PRIORITY 3: R3 – CUSTOMER IDENTITY MISMATCH
    # -------------------------------------------------------------
    if not clean_cust_id or clean_cust_id != registered_customer:
        return {
            "decision": BLOCK,
            "rule_id": "R3",
            "rule_name": "Customer Identity Mismatch",
            "reason": (
                f"The customer ID in the request ('{clean_cust_id}') does not match the customer ID "
                f"registered with this agent ('{registered_customer}'). Cross-customer operations "
                "are strictly prohibited for security and data privacy."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": canonical_action or str(action),
            "amount": amount,
        }

    # -------------------------------------------------------------
    # PRIORITY 4: R8 – INVALID OR UNAUTHORIZED REQUEST
    # -------------------------------------------------------------
    # Check for invalid action
    if canonical_action is None:
        return {
            "decision": BLOCK,
            "rule_id": "R8",
            "rule_name": "Invalid or Unauthorized Request",
            "reason": (
                f"The requested action '{action}' is invalid or unsupported by the Delta Air Lines "
                "Agent Gatekeeper API. Permitted actions are: View flight fares, Book flight, "
                "Change flight, and Request refund."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": str(action),
            "amount": amount,
        }

    # Check for negative transaction amount where applicable
    if amount is not None and amount < 0:
        return {
            "decision": BLOCK,
            "rule_id": "R8",
            "rule_name": "Invalid or Unauthorized Request",
            "reason": (
                f"The transaction amount (USD {amount}) is invalid. Negative amounts are rejected."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": canonical_action,
            "amount": amount,
        }

    # Check required permissions
    required_perm = REQUIRED_PERMISSIONS.get(canonical_action)
    if required_perm and not agent_permissions.get(required_perm, False):
        readable_perm = required_perm.replace("_", " ")
        return {
            "decision": BLOCK,
            "rule_id": "R8",
            "rule_name": "Invalid or Unauthorized Request",
            "reason": (
                f"The AI agent lacks the required '{readable_perm}' permission to perform "
                f"the action '{canonical_action}'. The customer has not granted this privilege."
            ),
            "execution_status": STATUS_BLOCKED,
            "normalized_action": canonical_action,
            "amount": amount,
        }

    # -------------------------------------------------------------
    # PRIORITY 5: R4 – VIEW FLIGHT FARES
    # -------------------------------------------------------------
    if canonical_action == "View flight fares":
        return {
            "decision": ALLOW,
            "rule_id": "R4",
            "rule_name": "View Flight Fares",
            "reason": (
                "The agent is registered, active, and authorized to view flight fares. "
                "Because this is a read-only search operation with no financial impact, "
                "the request is permitted."
            ),
            "execution_status": STATUS_EXECUTED,
            "normalized_action": canonical_action,
            "amount": amount,
        }

    # -------------------------------------------------------------
    # PRIORITY 6: R5 – BOOK FLIGHTS
    # -------------------------------------------------------------
    if canonical_action == "Book flight":
        # Missing amount check
        amt = amount if (amount is not None) else 0.0
        if amt <= BOOKING_DEMO_THRESHOLD_USD:
            return {
                "decision": ALLOW,
                "rule_id": "R5",
                "rule_name": "Book Flights (Under/At Demonstration Limit)",
                "reason": (
                    f"The active authorized agent requested a booking of USD {amt:.2f}, which is "
                    f"within the academic demonstration threshold of USD {BOOKING_DEMO_THRESHOLD_USD:.2f}. "
                    "The booking is pre-authorized and permitted."
                ),
                "execution_status": STATUS_EXECUTED,
                "normalized_action": canonical_action,
                "amount": amt,
            }
        else:
            return {
                "decision": ASK_CUSTOMER,
                "rule_id": "R5",
                "rule_name": "Book Flights (Exceeds Demonstration Limit)",
                "reason": (
                    f"The booking amount of USD {amt:.2f} exceeds the academic demonstration threshold "
                    f"of USD {BOOKING_DEMO_THRESHOLD_USD:.2f}. Explicit customer confirmation is required "
                    "before booking can be executed."
                ),
                "execution_status": STATUS_WAITING_CONFIRMATION,
                "normalized_action": canonical_action,
                "amount": amt,
            }

    # -------------------------------------------------------------
    # PRIORITY 7: R6 – CHANGE FLIGHTS
    # -------------------------------------------------------------
    if canonical_action == "Change flight":
        return {
            "decision": ASK_CUSTOMER,
            "rule_id": "R6",
            "rule_name": "Change Flights",
            "reason": (
                "Changing an existing flight booking alters travel itineraries and may incur fare "
                "differences or cancellation impacts. Customer confirmation is required before proceeding."
            ),
            "execution_status": STATUS_WAITING_CONFIRMATION,
            "normalized_action": canonical_action,
            "amount": amount,
        }

    # -------------------------------------------------------------
    # PRIORITY 8: R7 – REQUEST REFUND
    # -------------------------------------------------------------
    if canonical_action == "Request refund":
        return {
            "decision": ASK_CUSTOMER,
            "rule_id": "R7",
            "rule_name": "Request Refund",
            "reason": (
                "Refund processing impacts customer financial accounts and ticket validity. "
                "Explicit customer confirmation is required. Any processed refund remains subject to "
                "Delta Air Lines applicable fare rules and refund eligibility criteria."
            ),
            "execution_status": STATUS_WAITING_CONFIRMATION,
            "normalized_action": canonical_action,
            "amount": amount,
        }

    # Fallback for unexpected state
    return {
        "decision": BLOCK,
        "rule_id": "R8",
        "rule_name": "Invalid or Unauthorized Request",
        "reason": "Request could not be validated against standard business rules.",
        "execution_status": STATUS_BLOCKED,
        "normalized_action": str(action),
        "amount": amount,
    }
