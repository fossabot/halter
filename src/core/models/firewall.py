# models/firewall.py

from dataclasses import dataclass, field
from enum import StrEnum


class RuleAction(StrEnum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"
    FLUSH = "FLUSH"
    SET_POLICY = "SET_POLICY"


class Chain(StrEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    FORWARD = "FORWARD"


@dataclass(slots=True, kw_only=True)
class FirewallRule:
    chain: Chain
    action: RuleAction
    protocol: str | None = None
    source: str | None = None
    destination: str | None = None
    source_ports: list[int] | None = None
    destination_ports: list[int] | None = None
    interface_in: str | None = None
    interface_out: str | None = None
    state: str | None = None
    state_match: bool | None = None
    icmp_type: str | None = None
    tcp_flags: str | None = None
    policy: RuleAction | None = None
    table: str | None = None


@dataclass(slots=True, kw_only=True)
class FirewallConfig:
    rules: list[FirewallRule] = field(default_factory=list)
    default_policy_input: RuleAction = RuleAction.ACCEPT
    default_policy_forward: RuleAction = RuleAction.ACCEPT
    default_policy_output: RuleAction = RuleAction.ACCEPT
