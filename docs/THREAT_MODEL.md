# ANUBIS: Threat Model

This document outlines the core security threats targeted by ANUBIS and the specific architectural mitigations implemented.

| # | Threat | Description | Attacker Objective | ANUBIS Mitigation |
|---|---|---|---|---|
| **1** | **Credential Theft or Sharing** | Static API keys are hardcoded in prompts, committed to repos, or shared among multiple runtimes. | Steal static keys to gain persistent, untracked access to downstream services. | **Short-lived tokens bound to an agent instance (`instance_id` & `jti`).** Keypairs are used for challenge-response authentication. Downstream credentials never leave the gateway. |
| **2** | **Confused Deputy** | An agent with broad privileges is tricked by an unprivileged user or malicious content into executing actions on behalf of the wrong entity. | Force privileged agent to act for an unauthorized principal. | **Delegation chains and explicit `on_behalf_of` scoping.** Every call carries the human principal and lineage. |
| **3** | **Privilege Escalation** | A sub-agent attempts to request or acquire broader permissions than its delegating parent agent. | Break out of sub-agent sandbox to execute sensitive operations. | **Strict scope-subset rule (`child_scope ⊆ parent_scope`).** Token exchange validates that derived scopes can only narrow, never expand. |
| **4** | **Prompt-Injection-Driven Misuse** | Injected text in untrusted content manipulates the LLM into invoking dangerous tools (e.g. `send_email`, `delete_database`). | Manipulate agent logic via adversarial data. | **Policy engine (OPA/Rego) on tools and arguments, approval gates (`require_approval`), and rate limits.** |
| **5** | **Data Exfiltration** | An agent reads large volumes of sensitive records or forwards payloads to arbitrary external URLs. | Exfiltrate private data to an attacker-controlled endpoint. | **Volume rate limits, destination allowlists, credential isolation, and anomaly detection engine.** |
| **6** | **Rogue or Forgotten Agents** | Unmonitored, orphaned agents continue running indefinitely with active permissions. | Exploit abandoned agents as persistent backdoors. | **Mandatory agent registry with assigned owners, risk tiers, and hard expiration dates (`expires_at`).** |
| **7** | **Audit Log Tampering** | An attacker or compromised agent alters or deletes access logs to cover tracks. | Conceal unauthorized activity and prevent forensic discovery. | **Append-only cryptographic hash chaining (`prev_hash`).** Periodic public anchoring or signing of checkpoints. `/audit/verify` integrity check. |
| **8** | **Token Replay & Hijacking** | An intercepted token is replayed by an unauthorized actor or external process. | Use stolen token in another environment. | **Short TTL (5–15 mins), unique token IDs (`jti`), and strict instance binding.** |

---

## Security Invariants
1. **Fail Closed:** If policy evaluation, token verification, or revocation lookups fail or time out, the request is denied.
2. **Zero Raw Secret Exposure:** Agents never receive raw downstream credentials; the ANUBIS Gateway acts as the credential broker.
3. **Monotonic Scope Narrowing:** In any delegation chain $A \to B \to C$, $Scope(C) \subseteq Scope(B) \subseteq Scope(A)$.
4. **Non-Repudiation:** Every action links cryptographically to an accountable agent keypair, human owner, and trace ID.
