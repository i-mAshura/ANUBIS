# ANUBIS: Problem Statement

## The Rise of Autonomous AI Agents
Autonomous AI agents are shifting computing from direct human invocation to delegated autonomy. Today's AI agents:
- Execute external tools (APIs, command lines, database queries, web scrapers).
- Ingest unstructured, untrusted context from web pages, files, and incoming messages.
- Chain actions together and dynamically spawn sub-agents to divide and conquer tasks.

## The Core Problem
Despite their autonomy, agent security currently mirrors early microservice security or pre-cloud credentials:
1. **Shared & Static API Keys:** Agents are routinely given static API keys with broad, organization-wide privileges. If an agent key is leaked, the blast radius is total.
2. **Missing Agent Identity:** Current systems identify the *human* developer or a generic *service account*, but cannot identify individual agents or ephemeral agent instances.
3. **No Granular Scoping:** Once an agent has an API token, it has blanket access to every endpoint covered by that key.
4. **Untracked Delegation Chains:** When Agent A delegates a task to Sub-Agent B, which delegates to Sub-Agent C, attribution is lost. There is no cryptographic proof of who authorized what.
5. **Vulnerability to Prompt Injection:** Malicious inputs can hijack agent tool execution ("confused deputy" problem). Without external policy gates, the agent executes unauthorized tools or sends data to malicious endpoints.
6. **No Tamper-Evident Accountability:** Logs are easily tampered with or lack end-to-end trace correlation across agent sub-tasks.
7. **Absence of Real-Time Kill Switches:** Revoking a misbehaving agent often requires revoking the entire shared developer API key, causing widespread service disruption.

## The ANUBIS Solution
**ANUBIS** (*Agent Namespace, Unified Boundaries, Identity and Surveillance*) establishes a dedicated Zero-Trust **Identity and Control Plane** for AI agents.

By standing between agents and the resources they touch, ANUBIS enforces:
- **First-Class Agent Identity:** Every agent and running instance is cryptographically registered with explicit human ownership.
- **Task-Scoped Ephemeral Credentials:** Agents receive short-lived, instance-bound tokens (valid for minutes) scoped strictly to the current task.
- **Hierarchical Delegation Tracking:** Delegations form cryptographically attested `act` chains where child permissions must always be a subset of parent permissions.
- **Policy Enforcement & Credential Brokering:** Tools are accessed via the ANUBIS enforcement gateway (e.g. MCP proxy). Agents never touch raw downstream secrets.
- **Append-Only, Hash-Chained Audit Logs:** Every action and policy decision is recorded in a tamper-evident audit log that can be verified mathematically.
- **Instant Revocation (Kill Switch):** Compromised or misbehaving agents, instances, or tasks can be halted within seconds.
