"""
Agent Gatekeeper – AI Agent Permission and Access Control System for Delta Air Lines
Student: Veerparam Chauhan | Enrolment Number: PGD202563340
Industry: Airline | Company: Delta Air Lines

Module: gatekeeper.py
Purpose: Core gatekeeper engine that evaluates agent requests against business rules,
determines the decision (ALLOW, ASK CUSTOMER, BLOCK), tracks execution status,
and writes immutable audit  entries.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from rules import evaluate_rules
import storage


class AgentGatekeeper:
    """
    Core Gatekeeper engine instance.
    Can be initialized with custom data paths for testing or default paths for production.
    """

    def __init__(
        self,
        agents_file: Optional[Path] = None,
        audit_file: Optional[Path] = None
    ):
        self.agents_file = Path(agents_file) if agents_file else storage.DEFAULT_AGENTS_FILE
        self.audit_file = Path(audit_file) if audit_file else storage.DEFAULT_AUDIT_LOG_FILE

    def evaluate_request(
        self,
        customer_id: str,
        agent_identifier: str,
        action: str,
        amount: Optional[float] = None,
        record_audit: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluates an AI agent request.

        Steps:
        1. Query agent registration from storage.
        2. Evaluate against business rules in priority order (R1 -> R2 -> R3 -> R8 -> R4 -> R5 -> R6 -> R7).
        3. If record_audit is True, append an immutable audit log entry (JSONL).
        4. Return full decision package including execution status.
        """
        clean_cust_id = str(customer_id).strip() if customer_id else ""
        clean_agent_ident = str(agent_identifier).strip() if agent_identifier else ""

        # 1. Lookup agent
        agent = storage.find_agent(
            identifier=clean_agent_ident,
            customer_id=clean_cust_id,
            agents_file=self.agents_file
        )

        agent_status_at_request = agent.get("status", "UNKNOWN") if agent else "UNKNOWN"
        agent_id_resolved = agent.get("agent_id", "N/A") if agent else "N/A"
        agent_name_resolved = agent.get("agent_name", clean_agent_ident or "Unknown Agent") if agent else clean_agent_ident

        # 2. Evaluate business rules
        rule_result = evaluate_rules(
            agent=agent,
            customer_id=clean_cust_id,
            action=action,
            amount=amount
        )

        decision = rule_result["decision"]
        rule_id = rule_result["rule_id"]
        rule_name = rule_result["rule_name"]
        reason = rule_result["reason"]
        execution_status = rule_result["execution_status"]
        canonical_action = rule_result.get("normalized_action", action)

        # 3. Write immutable audit log
        audit_entry = None
        if record_audit:
            audit_entry = storage.log_event(
                event_type="request_evaluation",
                customer_id=clean_cust_id,
                agent_id=agent_id_resolved,
                agent_name=agent_name_resolved,
                action=canonical_action,
                amount=amount,
                decision=decision,
                rule_id=rule_id,
                reason=reason,
                agent_status=agent_status_at_request,
                audit_file=self.audit_file
            )

        # 4. Construct response dictionary
        return {
            "decision": decision,
            "rule_id": rule_id,
            "rule_name": rule_name,
            "reason": reason,
            "execution_status": execution_status,
            "customer_id": clean_cust_id,
            "agent_id": agent_id_resolved,
            "agent_name": agent_name_resolved,
            "action": canonical_action,
            "amount": amount,
            "agent_status": agent_status_at_request,
            "audit_event_id": audit_entry.get("event_id") if audit_entry else None
        }


# Convenience module-level function for direct evaluation
def check_request(
    customer_id: str,
    agent_identifier: str,
    action: str,
    amount: Optional[float] = None,
    agents_file: Optional[Path] = None,
    audit_file: Optional[Path] = None,
    record_audit: bool = True
) -> Dict[str, Any]:
    """Convenience helper to evaluate request without creating class instance."""
    gatekeeper = AgentGatekeeper(agents_file=agents_file, audit_file=audit_file)
    return gatekeeper.evaluate_request(
        customer_id=customer_id,
        agent_identifier=agent_identifier,
        action=action,
        amount=amount,
        record_audit=record_audit
    )
