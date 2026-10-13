package anubis.authz

import future.keywords.in
import future.keywords.if

default decision = "deny"
default reason = "Default deny: no matching allow rule"

# Allow read tools if token has tools:read scope
decision = "allow" if {
    "tools:read" in input.token.scope
    startswith(input.action.tool, "read_")
    reason = "Tool read allowed by tools:read scope"
}

# Allow email sending only to internal domain (@corp.local)
decision = "allow" if {
    "tools:email" in input.token.scope
    input.action.tool == "send_email"
    endswith(input.action.arguments.recipient, "@corp.local")
    reason = "Internal email allowed"
}

# Require human approval for external email
decision = "require_approval" if {
    "tools:email" in input.token.scope
    input.action.tool == "send_email"
    not endswith(input.action.arguments.recipient, "@corp.local")
    reason = "External email recipients require human approval"
}

# High-value financial transactions require human approval
decision = "require_approval" if {
    "tools:finance" in input.token.scope
    input.action.tool == "execute_transfer"
    input.action.arguments.amount > 5000
    reason = "Transactions exceeding $5,000 require human authorization"
}

# Small financial transactions allowed with tools:finance scope
decision = "allow" if {
    "tools:finance" in input.token.scope
    input.action.tool == "execute_transfer"
    input.action.arguments.amount <= 5000
    reason = "Transaction within permitted threshold"
}

# Outright deny for shell execution on low-tier agents
decision = "deny" if {
    input.action.tool == "system_shell"
    input.agent.risk_tier != "critical"
    reason = "System shell execution prohibited for non-critical tier agents"
}
