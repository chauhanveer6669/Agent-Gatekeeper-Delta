"""
Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines
Student: Veerparam Chauhan | Enrolment Number: PGD202563340
Industry: Airline | Company: Delta Air Lines

Module: storage.py
Purpose: Handles persistent storage for AI agent registrations (JSON) and
immutable audit trail event logs (JSON Lines / JSONL).
"""

import os
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

# Default storage paths relative to this file
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = BASE_DIR / "data"
DEFAULT_AGENTS_FILE = DEFAULT_DATA_DIR / "agents.json"
DEFAULT_AUDIT_LOG_FILE = DEFAULT_DATA_DIR / "audit_log.jsonl"


def _ensure_dir_exists(file_path: Path):
    """Ensures parent directory for given file path exists."""
    os.makedirs(file_path.parent, exist_ok=True)


def get_current_iso_timestamp() -> str:
    """Returns current date and time in ISO 8601 format with timezone offset."""
    return datetime.now(timezone.utc).astimezone().isoformat()


# -------------------------------------------------------------------
# AGENTS STORAGE (JSON)
# -------------------------------------------------------------------

def load_agents(file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Loads all registered agents from JSON file.
    Returns an empty list if the file does not exist or is empty.
    """
    target = Path(file_path) if file_path else DEFAULT_AGENTS_FILE
    if not target.exists():
        return []
    try:
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_agents(agents: List[Dict[str, Any]], file_path: Optional[Path] = None) -> bool:
    """
    Saves the list of registered agents to JSON file with indentation.
    """
    target = Path(file_path) if file_path else DEFAULT_AGENTS_FILE
    _ensure_dir_exists(target)
    try:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(agents, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def find_agent(
    identifier: str,
    customer_id: Optional[str] = None,
    agents_file: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """
    Finds an agent by agent_id or agent_name.
    If customer_id is provided, prefers an exact match on customer_id + identifier.
    """
    if not identifier:
        return None
    agents = load_agents(agents_file)
    ident_clean = identifier.strip().lower()
    cust_clean = customer_id.strip() if customer_id else None

    # First pass: check for exact customer_id + (agent_id OR agent_name) match
    if cust_clean:
        for a in agents:
            if a.get("customer_id", "").strip() == cust_clean:
                if (a.get("agent_id", "").strip().lower() == ident_clean or
                        a.get("agent_name", "").strip().lower() == ident_clean):
                    return a

    # Second pass: check agent_id match across all
    for a in agents:
        if a.get("agent_id", "").strip().lower() == ident_clean:
            return a

    # Third pass: check agent_name match across all
    for a in agents:
        if a.get("agent_name", "").strip().lower() == ident_clean:
            return a

    return None


def register_agent(
    customer_id: str,
    agent_name: str,
    permissions: Dict[str, bool],
    customer_name: Optional[str] = "",
    agents_file: Optional[Path] = None,
    audit_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Registers a new AI agent with ACTIVE status, generates unique Agent ID,
    persists to JSON, and records a 'registration' event in the audit log.

    Prevents duplicate active registration for the same customer and agent name.
    """
    clean_cust_id = customer_id.strip()
    clean_agent_name = agent_name.strip()
    clean_cust_name = customer_name.strip() if customer_name else ""

    if not clean_cust_id:
        raise ValueError("Customer ID is required.")
    if not clean_agent_name:
        raise ValueError("Agent name is required.")

    agents = load_agents(agents_file)

    # Check for duplicate registration (same customer ID + same agent name)
    for a in agents:
        if (a.get("customer_id", "").strip() == clean_cust_id and
                a.get("agent_name", "").strip().lower() == clean_agent_name.lower()):
            if a.get("status") == "ACTIVE":
                return {
                    "success": False,
                    "error": f"Agent '{clean_agent_name}' is already registered and ACTIVE for Customer '{clean_cust_id}'.",
                    "agent": a
                }

    # Generate unique Agent ID
    unique_suffix = uuid.uuid4().hex[:6].upper()
    agent_id = f"DAL-AGT-{unique_suffix}"
    registration_time = get_current_iso_timestamp()

    # Standardize permissions dict
    standard_permissions = {
        "view_fares": bool(permissions.get("view_fares", False)),
        "book_flights": bool(permissions.get("book_flights", False)),
        "change_flights": bool(permissions.get("change_flights", False)),
        "request_refunds": bool(permissions.get("request_refunds", False)),
    }

    new_agent = {
        "agent_id": agent_id,
        "agent_name": clean_agent_name,
        "customer_id": clean_cust_id,
        "customer_name": clean_cust_name,
        "status": "ACTIVE",
        "registered_at": registration_time,
        "revoked_at": None,
        "revoked_by": None,
        "permissions": standard_permissions
    }

    agents.append(new_agent)
    save_agents(agents, agents_file)

    # Log registration event
    log_event(
        event_type="registration",
        customer_id=clean_cust_id,
        agent_id=agent_id,
        agent_name=clean_agent_name,
        action="Register Agent",
        amount=None,
        decision="ALLOW",
        rule_id="SYS-REG",
        reason=f"AI Agent '{clean_agent_name}' successfully registered with ACTIVE status and specified permissions.",
        agent_status="ACTIVE",
        audit_file=audit_file
    )

    return {
        "success": True,
        "message": f"AI Agent '{clean_agent_name}' ({agent_id}) successfully registered.",
        "agent": new_agent
    }


def revoke_agent(
    agent_id: str,
    revoked_by: str = "Customer (via Delta Portal)",
    agents_file: Optional[Path] = None,
    audit_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Revokes an agent's access:
    - Changes status to REVOKED
    - Sets exact ISO 8601 revocation timestamp with timezone
    - Records who performed revocation
    - Preserves all original registration data (NEVER deletes)
    - Records revocation event in audit log
    """
    clean_id = agent_id.strip().lower()
    agents = load_agents(agents_file)
    target_agent = None

    for a in agents:
        if a.get("agent_id", "").strip().lower() == clean_id:
            target_agent = a
            break

    if not target_agent:
        return {
            "success": False,
            "error": f"Agent with ID '{agent_id}' was not found in registration records."
        }

    if target_agent.get("status") == "REVOKED":
        return {
            "success": False,
            "error": f"Agent '{target_agent.get('agent_name')}' ({target_agent.get('agent_id')}) is already REVOKED.",
            "agent": target_agent
        }

    revocation_timestamp = get_current_iso_timestamp()
    target_agent["status"] = "REVOKED"
    target_agent["revoked_at"] = revocation_timestamp
    target_agent["revoked_by"] = revoked_by

    save_agents(agents, agents_file)

    # Log revocation event
    log_event(
        event_type="revocation",
        customer_id=target_agent.get("customer_id"),
        agent_id=target_agent.get("agent_id"),
        agent_name=target_agent.get("agent_name"),
        action="Revoke Access",
        amount=None,
        decision="BLOCK",
        rule_id="R2",
        reason=f"Customer revoked AI Agent access. Revoked by: {revoked_by}. All future requests will be blocked.",
        agent_status="REVOKED",
        audit_file=audit_file
    )

    return {
        "success": True,
        "message": f"Agent '{target_agent.get('agent_name')}' ({target_agent.get('agent_id')}) has been permanently REVOKED.",
        "revoked_at": revocation_timestamp,
        "agent": target_agent
    }


# -------------------------------------------------------------------
# AUDIT LOG STORAGE (JSON LINES / JSONL)
# -------------------------------------------------------------------

def log_event(
    event_type: str,
    customer_id: Optional[str],
    agent_id: Optional[str],
    agent_name: Optional[str],
    action: str,
    amount: Optional[float],
    decision: str,
    rule_id: str,
    reason: str,
    agent_status: str,
    audit_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Appends an immutable audit event to the JSONL log file.
    Never overwrites historical records.
    """
    target = Path(audit_file) if audit_file else DEFAULT_AUDIT_LOG_FILE
    _ensure_dir_exists(target)

    event_id = f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
    timestamp = get_current_iso_timestamp()

    event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "event_type": event_type,  # 'registration', 'request_evaluation', 'revocation'
        "customer_id": customer_id or "N/A",
        "agent_id": agent_id or "N/A",
        "agent_name": agent_name or "N/A",
        "action": action,
        "amount": round(float(amount), 2) if amount is not None else None,
        "decision": decision,
        "rule_id": rule_id,
        "reason": reason,
        "agent_status": agent_status
    }

    try:
        with open(target, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError as e:
        # Non-fatal logging error handling
        pass

    return event


def load_audit_logs(audit_file: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Reads all audit log records from the JSONL file.
    Returns an empty list if file does not exist.
    """
    target = Path(audit_file) if audit_file else DEFAULT_AUDIT_LOG_FILE
    if not target.exists():
        return []

    logs = []
    try:
        with open(target, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str:
                    try:
                        record = json.loads(line_str)
                        logs.append(record)
                    except json.JSONDecodeError:
                        continue
    except OSError:
        return []
    return logs


def get_audit_dataframe(audit_file: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads audit records and returns a clean, formatted Pandas DataFrame.
    """
    records = load_audit_logs(audit_file)
    if not records:
        return pd.DataFrame(columns=[
            "event_id", "timestamp", "event_type", "customer_id",
            "agent_id", "agent_name", "action", "amount",
            "decision", "rule_id", "reason", "agent_status"
        ])
    df = pd.DataFrame(records)
    return df


def get_metrics(agents_file: Optional[Path] = None, audit_file: Optional[Path] = None) -> Dict[str, int]:
    """
    Calculates summary metrics for dashboard display:
    - total_agents
    - active_agents
    - revoked_agents
    - total_requests
    - allow_decisions
    - ask_customer_decisions
    - block_decisions
    """
    agents = load_agents(agents_file)
    total_agents = len(agents)
    active_agents = sum(1 for a in agents if a.get("status") == "ACTIVE")
    revoked_agents = sum(1 for a in agents if a.get("status") == "REVOKED")

    logs = load_audit_logs(audit_file)
    request_evals = [e for e in logs if e.get("event_type") == "request_evaluation"]
    total_requests = len(request_evals)

    allow_count = sum(1 for e in request_evals if e.get("decision") == "ALLOW")
    ask_count = sum(1 for e in request_evals if e.get("decision") == "ASK CUSTOMER")
    block_count = sum(1 for e in request_evals if e.get("decision") == "BLOCK")

    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "revoked_agents": revoked_agents,
        "total_requests": total_requests,
        "allow_decisions": allow_count,
        "ask_customer_decisions": ask_count,
        "block_decisions": block_count
    }


def init_default_data_if_empty(agents_file: Optional[Path] = None, audit_file: Optional[Path] = None):
    """
    Pre-populates demonstration data (e.g. TravelBot) if storage is completely empty,
    allowing immediate exploration while preserving academic integrity.
    """
    target_agents = Path(agents_file) if agents_file else DEFAULT_AGENTS_FILE
    target_audit = Path(audit_file) if audit_file else DEFAULT_AUDIT_LOG_FILE

    _ensure_dir_exists(target_agents)
    _ensure_dir_exists(target_audit)

    if not target_agents.exists() or os.path.getsize(target_agents) == 0:
        # Create empty list first
        save_agents([], target_agents)
        # Register standard demo agent TravelBot
        register_agent(
            customer_id="CUST001",
            agent_name="TravelBot",
            permissions={
                "view_fares": True,
                "book_flights": True,
                "change_flights": True,
                "request_refunds": True,
            },
            customer_name="Veerparam Chauhan",
            agents_file=target_agents,
            audit_file=target_audit
        )
