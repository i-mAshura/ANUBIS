# 𓁢 A N U B I S
### *The Obsidian Control Plane: Cryptographic Necromancy, Zero-Trust IAM & Abyssal Surveillance for Autonomous AI Agents*

<p align="center">
  <img src="https://img.shields.io/badge/HELLFIRE-ACTIVE%20CONFLAGRATION-800000?style=for-the-badge&logo=ghostery&logoColor=red" alt="Hellfire Active" />
  <img src="https://img.shields.io/badge/JUDGMENT-FAIL--CLOSED%20GUILLOTINE-000000?style=for-the-badge&logo=shield&logoColor=crimson" alt="Guillotine Fail-Closed" />
  <img src="https://img.shields.io/badge/SCALES_OF_MAAT-ES256%20ECDSA%20P--256-4a0000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="ES256 ECDSA" />
  <img src="https://img.shields.io/badge/AUDIT_LEDGER-SHA--256%20HASH--CHAINED-1a0000?style=for-the-badge&logo=git&logoColor=darkred" alt="Hash-Chained Audit" />
  <img src="https://img.shields.io/badge/SOULS_WEIGHED-51%2F51%20TRIALS%20PASSED-330000?style=for-the-badge&logo=checkmarx&logoColor=lime" alt="51 Tests Passed" />
  <img src="https://img.shields.io/badge/LICENSE-APACHE_2.0-550000?style=for-the-badge" alt="License" />
</p>

```
                                      /\
                                     /  \
                                    / /\ \
                                   / /  \ \
                                  / /    \ \
                                 / /      \ \
              __________________/ /________\ \__________________
             |                                                  |
             |       .---.          .-----------.          .---.|
             |      /     \        /             \        /     \
             |     | () () |      |  𓁢  ANUBIS  𓁢 |      | () () |
             |      \  _  /        \   JUDGES    /        \  _  /
             |       `---'          `-----------'          `---'|
             |      /| | |\               |               /| | |\
             |     / |_|_| \              ▼              / |_|_| \
             |    /  \___/  \       [ THE SCALES ]      /  \___/  \
             |__________________________________________________|
                           ||                                ||
                [ THE HEART OF THE AGENT ]      [ THE FEATHER OF TRUTH ]
                           ||                                ||
                           \==================================/
                                            ||
                                            ▼
                     "EVERY AGENT IS WEIGHED BEFORE IT PASSES,
                      AND IN THE UNDERWORLD, THE RECORD NEVER LIES."
```

---

## 🩸 The Decrees of the Necropolis: The Horrific Reality of AI Autonomy

In the mortal plane of software architecture, unbaptized autonomous AI agents roam like fleshless wraiths. They are handed almighty static master credentials; they burrow through production databases; they whisper prompt-injected incantations in the shadows; and they spawn recursive swarms of ungoverned sub-demons. When prompt injection strikes, the blast radius is absolute—**because the agent has no immutable birthmark, no cryptographic boundary, and no judge.**

**ANUBIS** is the black obsidian control plane that stands at the mouth of the abyss. Named after the jackal-headed god of embalming and the afterlife who extracts the mortal heart and balances it upon the Golden Scales against the Feather of Truth:

> ⚖️ **If an agent’s token is unblemished, its cryptographic lineage pure, and its scope monotonically restricted: It may pass.**  
> ⚔️ **If its heart is weighed down with forged scopes, stolen tokens, anomalous tool probing, or prompt injection: Anubis drops the guillotine blade. Execution is severed in milliseconds, the entity is hurled into the jaws of Ammit, and the damnation is branded forever into the immutable ledgers of the dead.**

---

## 🏛️ The Infernal Architecture: Bifurcation of Planes

ANUBIS enforces a mathematical air-gap between the ethereal plane of governance (**Control Plane**) and the iron gates of physical execution (**Data Plane**):

```
                        [ MORTAL OVERSEERS & SEC-OPS ALTAR ]
                                         │
                                         ▼
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                 THE ANUBIS CONTROL PLANE (Port 8000)             ║
    ║                                                                   ║
    ║  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  ║
    ║  │ AGENT REGISTRY  │   │  AUTH & TOKENS  │   │  POLICY ENGINE  │  ║
    ║  │ The Crypt of    │   │ The Weighing of │   │ The Scales of   │  ║
    ║  │  Living Souls   │   │  the Heart Nonce│   │  Ma'at (OPA)    │  ║
    ║  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘  ║
    ║           │                     │                     │           ║
    ║  ┌────────┴────────┐   ┌────────┴────────┐   ┌────────┴────────┐  ║
    ║  │ TASK DELEGATION │   │ APPROVAL QUEUE  │   │ DETECTION ENGINE│  ║
    ║  │ Monotonic Scope │   │ The Plea for    │   │ The Scourge of  │  ║
    ║  │  Lineage Tree   │   │  Human Mercy    │   │  Ammit (Anom)   │  ║
    ║  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘  ║
    ║           │                     │                     │           ║
    ║           ▼                     ▼                     ▼           ║
    ║  ┌─────────────────────────────────────────────────────────────┐  ║
    ║  │ PostgreSQL (Relational Core)  │ Redis (Instant Damnation)   │  ║
    ║  └─────────────────────────────────────────────────────────────┘  ║
    ╚═══════════════════════════════════════════════════════════════════╝
                                      ▲
                                      │ 𓋹 Ephemeral ES256 JWTs / JWKS
                                      │ 𓋒 Instant Multi-Vector Revocation
                                      ▼
  ┌───────────────┐       ┌───────────────────────┐       ┌────────────────┐
  │ AUTONOMOUS    │       │   THE OBSIDIAN GATE   │       │ DOWNSTREAM     │
  │ AI AGENT      ├──────►│ (MCP JSON-RPC Proxy)  ├──────►│ PRODUCTION APIS│
  │ (The Pilgrim) │       │                       │       │ SECRETS & TOOLS│
  └───────────────┘       │ • Credential Broker   │       └────────────────┘
                          │ • Secret Redaction    │
                          │ • Fail-Closed Guard   │
                          └───────────┬───────────┘
                                      │
                                      ▼
                          ┌───────────────────────┐
                          │   THE BOOK OF THE DEAD│
                          │ (Append-Only, Hash-   │
                          │  Chained Audit Trail) │
                          └───────────────────────┘
```

---

## ⚔️ The Seven Pillars of Eternal Retribution: Mathematical Formalisms

```
               [ I. ATOMIC CRYPTOGRAPHIC IDENTITY ]
                         │   agt_<sha256_spki_fingerprint>
                         ▼
               [ II. THE WEIGHING OF THE HEART ]
                         │   Nonce signed with local ECDSA P-256 key
                         ▼
               [ III. MONOTONIC SCOPE COLLAPSE ]
                         │   Scope(child) ⊆ Scope(parent); 'act' lineage chain
                         ▼
               [ IV. THE OBSIDIAN GUILLOTINE ]
                         │   P(Execution | Policy Error) ≡ 0 (Fail-Closed)
                         ▼
               [ V. THE CANOPIC JARS OF SECRETS ]
                         │   Brokered downstream credentials; raw secret redaction
                         ▼
               [ VI. THE BOOK OF THE DEAD ]
                         │   Hash_n = SHA-256(Record_n || Hash_{n-1})
                         ▼
               [ VII. THE SCOURGE OF AMMIT ]
                             Sliding-window denial burst → 5-Vector Kill Switch
```

---

### Pillar I. 𓋹 The Crypt of Souls: Atomic Cryptographic Identity
No nameless phantom may cross the River of Fire. At registration (`POST /agents`), an agent cannot pick an arbitrary identity. Its unique identifier is derived **atomically** from the mathematical fingerprint of its public key under the NIST P-256 elliptic curve:

```text
  Curve: E(F_p) : y^2 ≡ x^3 - 3x + b (mod p)   [NIST P-256 / secp256r1]
  Agent ID = "agt_" || Trunc_24( Hex( SHA-256( SubjectPublicKeyInfo_DER ) ) )
```

$$\mathbf{ID}(a) = \texttt{"agt\_"} \mathbin{\Vert} \mathrm{Trunc}_{24}\Big(\mathrm{Hex}\big(\mathrm{SHA256}(\mathrm{DER}(K_{\mathrm{pub}}))\big)\Big)$$

* **Theorem of Soul Uniqueness:** Given the collision-resistance of $\mathrm{SHA256}$, the probability of two rogue agents generating colliding identities is bounded by $\mathcal{O}(2^{-128})$.
* **Zero-Knowledge Principle:** The private key $K_{\mathrm{priv}}$ is generated and kept inside the agent's memory boundary. The ANUBIS control plane **never** possesses the private key.

---

### Pillar II. 𓇯 The Weighing of the Heart: Challenge-Response Ritual
Static bearer secrets are an abomination. When an agent demands tool execution, it must prove its life through cryptographic sacrifice:

1. **The Nonce Incantation:** The agent requests a cryptographically secure, unpredictable 256-bit challenge nonce:
$$\mathcal{N} \leftarrow_{\mathrm{R}} \{0,1\}^{256}, \quad \mathrm{TTL}(\mathcal{N}) \le 300\text{ seconds}$$
2. **The Signature of Flesh:** The agent signs the nonce using its private key:
$$\sigma = \mathrm{Sign}_{K_{\mathrm{priv}}}(\mathcal{N})$$
3. **The Issuance of Ephemeral Life:** ANUBIS validates $\mathrm{Verify}_{K_{\mathrm{pub}}}(\mathcal{N}, \sigma) = 1$. Upon verification, the nonce is burned forever and an ephemeral instance-bound **ES256 JWT** is minted:
$$\mathcal{T}_{\mathrm{jwt}} = \mathrm{Sign}_{\mathrm{ANUBIS}}\Big(\mathrm{sub}=\mathbf{ID}(a), \, \mathrm{jti}=\mu, \, \mathrm{exp}=t_{\mathrm{now}} + 900\mathrm{s}, \, \mathrm{scope}=\mathcal{S}\Big)$$

* **Replay Immunity:** Replayed challenges are consumed by hellfire. Intercepted tokens expire within 15 minutes.

---

### Pillar III. 𓍝 The Scales of Ma'at: Monotonic Scope Collapse & Lineage
When an autonomous agent delegates work to a child sub-agent (`POST /auth/exchange`), it can **never** grant more authority than it holds. Authority is subject to monotonic entropy collapse:

```text
  Scope(Child Agent) ⊆ Scope(Parent Agent)
  ∀ s ∈ Scope(Child): s ∈ Scope(Parent)
  |Scope(Child)| ≤ |Scope(Parent)|
```

$$\mathcal{S}_{\mathrm{child}} \subseteq \mathcal{S}_{\mathrm{parent}} \quad \iff \quad \forall s \in \mathcal{S}_{\mathrm{child}}, \; s \in \mathcal{S}_{\mathrm{parent}}$$

* **Privilege Escalation Impossibility:** If $\exists s \in \mathcal{S}_{\mathrm{child}}$ such that $s \notin \mathcal{S}_{\mathrm{parent}}$, the request is rejected with `HTTP 403 Forbidden`.
* **The Ancestral Actor Chain (`act`):** The cryptographic lineage vector is appended monotonically into the token payload:
$$\mathbf{act}_{k} = \big[ \mathbf{ID}(a_0), \, \mathbf{ID}(a_1), \, \dots, \, \mathbf{ID}(a_k) \big]$$
Downstream tools inspect not merely the immediate caller, but the entire ancestral bloodline of agents.

---

### Pillar IV. 𓆣 The Obsidian Guillotine: Fail-Closed Gateway Invariant
Every Model Context Protocol (MCP) tool execution request (`POST /mcp/{server}`) must pass under the razor edge of the Obsidian Gate.

* **The Fail-Closed Mathematical Invariant:**
$$\mathbb{P}\big(\text{Tool Execution} \mid \text{Policy Timeout} \lor \text{Network Outage} \lor \text{Rego Error}\big) \equiv 0$$

If the Open Policy Agent (OPA) engine times out ($\tau > 50\text{ms}$), if policy rules fail to compile, or if a cryptographic signature is malformed by a single bit, the guillotine drops. The default state of the universe is **DENY**.

---

### Pillar V. 𓋖 The Canopic Jars of Secrets: Downstream Credential Isolation
Agents must never touch, store, or view master credentials, database passwords, or third-party API keys:

1. **Vault Isolation:** Downstream secrets reside strictly in the encrypted vaults of ANUBIS.
2. **Credential Brokering:** ANUBIS injects secrets directly into downstream tool executions on behalf of the agent.
3. **Mutilation & Redaction:** Outgoing tool responses are scrubbed with regex and string sanitizers:
$$\mathrm{Response}_{\mathrm{sanitized}} = \mathrm{ScrubSecrets}\big(\mathrm{Response}_{\mathrm{raw}}, \; \mathcal{V}_{\mathrm{secrets}}\big)$$
Raw database tokens, passwords, and private keys can never leak into LLM context windows or conversation logs.

---

### Pillar VI. 𓉣 The Book of the Dead: Cryptographic Hash-Chained Necrology
Every single tool attempt, argument payload, verdict, latency measurement, and error is inscribed into an append-only cryptographic ledger chained by `SHA-256`:

```text
  H_0 = 0000000000000000000000000000000000000000000000000000000000000000
  H_i = SHA-256( CanonicalJSON( Event_i ) || H_{i-1} )    ∀ i ≥ 1
```

$$H_i = \mathrm{SHA256}\Big(\mathrm{CanonicalJSON}(\mathcal{E}_i) \mathbin{\Vert} H_{i-1}\Big)$$

* **Tamper Evident:** If an insider, attacker, or compromised root account alters a single character in record $k$, the chain breaks for all subsequent records $j \ge k$:
$$\exists k : H_k \ne \mathrm{SHA256}\big(\mathcal{E}_k \mathbin{\Vert} H_{k-1}\big) \implies \text{Tamper Alarm Triggered}$$
A single call to `GET /audit/verify` detects mathematical corruption in milliseconds.

---

### Pillar VII. 𓌃 The Scourge of Ammit: Denial Bursts & 5-Dimensional Kill Switch
The Detection Engine monitors rolling sliding-window telemetry buffers for each active soul:

1. **Denial Burst Anomaly Rule:**
$$\mathcal{D}(a, \Delta t) = \sum_{t_i \in [t_{\mathrm{now}} - \Delta t, \, t_{\mathrm{now}}]} \mathbb{I}\Big(\mathrm{Verdict}(a, t_i) = \text{DENY}\Big)$$
$$\text{If } \mathcal{D}(a, 60\mathrm{s}) \ge 5 \implies \mathrm{Action}(a) \leftarrow \text{CRITICAL SUSPENSION}$$

2. **Automated Multi-Vector Retribution:** The agent is suspended in the registry, and an immediate blacklist entry is injected into the **5-Dimensional Kill Switch Manifold**:
$$\mathbf{K} \subseteq \mathcal{A} \times \mathcal{I} \times \mathcal{T} \times \mathcal{J} \times \mathcal{P}$$

```text
  Revocation Manifold:
  {
    Agent ID:         agt_ca51d8ac48ed9d2f28ff05c5  (Terminates entire agent lineage)
    Instance ID:      inst-sec-1                    (Terminates specific container)
    Task ID:          task-detection-test           (Terminates task tree)
    Token JTI:        c82a19b0-4f81-49b2-9981       (Terminates specific JWT)
    Human Principal:  sec_admin                     (Terminates compromised human)
  }
```

Subsequent calls matching any point on this manifold are obliterated with `HTTP 403 Forbidden` in sub-millisecond lookups.

---

## 📜 The Complete Underworld Grimoire: Full API Blueprint

```http
### ==================== I. THE CRYPT OF SOULS (REGISTRY) ====================
POST   /owners                          # Inscribe accountable mortal master or team
GET    /owners                          # Enumerate all registered mortal owners
GET    /owners/{id}                     # Inspect specific owner details
POST   /agents                          # Inscribe agent (Atomic ES256 P-256 ID derivation)
GET    /agents                          # Enumerate agents (filter: active, suspended, revoked)
GET    /agents/{id}                     # Inspect agent identity & stored public key
PATCH  /agents/{id}                     # Mutate status (active -> suspended -> revoked)
POST   /agents/{id}/instances           # Bind ephemeral runtime execution container

### ==================== II. THE TRIAL OF PROOF (AUTH & TOKENS) ====================
POST   /auth/challenge                  # Generate cryptographically secure nonce challenge
POST   /auth/token                      # Verify ECDSA signature and mint task-scoped ES256 JWT
POST   /auth/exchange                   # Monotonic token exchange for delegated sub-agents
POST   /auth/keypair                    # Helper ritual: forge an ECDSA P-256 keypair
GET    /.well-known/jwks.json           # RFC 7517 JSON Web Key Set of ANUBIS signing keys

### ==================== III. THE SCALES OF MAAT (POLICY ENGINE) ====================
POST   /policies                        # Register declarative OPA/Rego governance rule
GET    /policies                        # List active policies in the underworld
POST   /policies/simulate               # Dry-run policy evaluation against hypothetical action

### ==================== IV. THE OBSIDIAN GATE (DATA PLANE MCP PROXY) ====================
POST   /tools                           # Register downstream tool, risk level & brokered secrets
GET    /tools                           # Enumerate registered tools and JSON argument schemas
POST   /mcp/{server}                    # Intercepted JSON-RPC 2.0 tool execution gateway

### ==================== V. THE BOOK OF THE DEAD (SURVEILLANCE & AUDIT) ====================
GET    /audit                           # Retrieve immutable audit events (agent, tool, outcome)
GET    /audit/verify                    # Mathematical SHA-256 hash-chain tamper detection check

### ==================== VI. TASKS & DELEGATION HIERARCHIES ====================
POST   /tasks                           # Create scoped task container for agent workflows
GET    /tasks                           # Enumerate tasks and subtask lineage
GET    /tasks/{id}                      # Inspect specific task status and delegation chain

### ==================== VII. PLEAS FOR MERCY (HUMAN APPROVALS) ====================
GET    /approvals                       # Enumerate pending approval requests
GET    /approvals/{id}                  # Inspect specific approval parameters
POST   /approvals/{id}/decision         # Render verdict: 'approved' or 'rejected'

### ==================== VIII. THE FIVE-VECTOR KILL SWITCH ====================
POST   /revocations                     # Blacklist by agent, instance, task, jti, or principal
GET    /revocations                     # Enumerate active damnation entries
POST   /revocations/check               # Microsecond revocation check query
DELETE /revocations/{id}                # Pardon/lift revocation entry

### ==================== IX. THE SCOURGE OF AMMIT (ANOMALY DETECTION) ====================
GET    /alerts                          # Query detection alerts (denial_burst, novel_tool_probe)
PATCH  /alerts/{id}                     # Triage alert: active -> acknowledged -> resolved
GET    /baselines/{agent_id}            # Inspect learned behavioral profile & call history
```

---

## 🐍 The Serpent's Grasp: Python SDK (`anubis.sdk`)

ANUBIS ships with a zero-dependency, ultra-secure Python SDK designed to govern any LLM agent framework (LangChain, AutoGen, CrewAI, or direct OpenAI/Anthropic tool runners).

### 1. Bootstrapping an Agent with Local Cryptographic Keys
```python
from anubis.sdk import AnubisAgent, AnubisClient
from anubis.sdk.exceptions import (
    AnubisPolicyDeniedError,
    AnubisApprovalRequiredError,
    AnubisKillSwitchError
)

# Connect to the ANUBIS Control Plane
client = AnubisClient(base_url="http://localhost:8000")

# Register an agent: Generates local ECDSA P-256 keys, derives agt_<hash>
agent = AnubisAgent(
    name="Orchestrator-Prime",
    owner_id="own_secops",
    purpose="Autonomous Financial Reconciliation",
    risk_tier="medium",
    capabilities=["tools:read", "tools:finance"],
    client=client
)

# Authenticate via cryptographic challenge-response
agent.bootstrap(scope=["tools:read", "tools:finance"])
print(f"Soul Awakened: {agent.agent_id}")
```

### 2. Invoking Mediated Tools Through the Obsidian Gate
```python
# MCP tool call mediated by OPA policy; downstream secrets brokered seamlessly
result = agent.execute_tool(
    server="corp-database",
    tool_name="read_records",
    arguments={"table": "quarterly_balance_sheets"}
)
print("Execution Result:", result)
```

### 3. Spawning Sub-Agents with Monotonic Scope Collapse
```python
# Sub-agent inherits narrowed scope and 'act' lineage chain
sub_agent = agent.spawn_subagent(
    name="Analyst-Sub01",
    purpose="Summarize balance sheets",
    task_intent="Data extraction from corporate records",
    delegated_scope=["tools:read"] # Monotonically narrowed: cannot transfer funds!
)

# Sub-agent executes permitted read tool
sub_result = sub_agent.execute_tool(
    server="corp-database",
    tool_name="read_records",
    arguments={"table": "income_statements"}
)

# Attempting an unauthorized tool triggers instant policy denial
try:
    sub_agent.execute_tool(
        server="bank-transfer",
        tool_name="execute_transfer",
        arguments={"amount": 1000}
    )
except AnubisPolicyDeniedError as err:
    print(f"[FAIL-CLOSED GUILLOTINE] Access Denied: {err.reason}")
```

### 4. Handling Human-in-the-Loop Hold-and-Resume
```python
try:
    # High-value operations trigger human supervisor approval
    agent.execute_tool(
        server="bank-transfer",
        tool_name="execute_transfer",
        arguments={"amount": 10000, "recipient": "vendor-corp"}
    )
except AnubisApprovalRequiredError as appr_err:
    print(f"Action Held! Approval ID: {appr_err.approval_id}")

    # Supervisor approves via portal or API:
    client.decide_approval(
        approval_id=appr_err.approval_id,
        decision="approved",
        approver_id="supervisor@corp.local",
        comment="Authorized quarterly vendor payment"
    )

    # Agent resumes seamlessly using the approval ticket
    resumed = agent.execute_tool(
        server="bank-transfer",
        tool_name="execute_transfer",
        arguments={"amount": 10000, "recipient": "vendor-corp"},
        approval_id=appr_err.approval_id
    )
    print("Resumed Action Success:", resumed)
```

---

## 🚀 The Ritual of Verification: Live Multi-Agent Workflow Demo

Execute the live demonstration harness showcasing the complete lifecycle:

```powershell
python examples/autonomous_research_workflow.py
```

```
======================================================================
  ANUBIS: Autonomous Agent Zero-Trust Architecture Demo
  'Every agent is weighed before it passes, and the record never lies.'
======================================================================

[1] Registering Corporate Owner...
    Owner Registered: Security & Compliance Office (own_33894)

[2] Registering MCP Tools on Gateway...
    Registered: 'read_financial_filings', 'send_email', 'execute_transfer'

[3] Bootstrapping Primary Agent (Orchestrator-Prime)...
    Agent ID Born: agt_ca51d8ac48ed9d2f28ff05c5 (derived from ECDSA P-256 fingerprint)
    Authentication Token Acquired (ES256 signed)

[4] Invoking 'read_financial_filings' through ANUBIS MCP Gateway...
    Success: executed
    Brokered Auth Used: True
    Zero-Trust Leakage Check: Raw secret scrubbed from response.

[5] Spawning Sub-Agent (Researcher-Sub01) with Scope-Narrowed Delegation...
    Sub-Agent ID Born: agt_3cd61dd8d630c289cc1da006
    Delegated Task ID: tsk_84bf92a188e2
    Lineage Chain ('act'): ['agt_ca51d8ac48ed9d2f28ff05c5', 'agt_3cd61dd8d630c289cc1da006']

[6] Sub-Agent executing permitted 'read_financial_filings'...
    Sub-Agent Status: executed

[7] Testing Privilege Escalation: Sub-Agent attempts 'execute_transfer' without scope...
    [BLOCKED] Zero-Trust Enforced: Default deny: no matching allow rule or required scope for tool 'execute_transfer'.

[8] High-Risk Tool Execution: Orchestrator attempts $7,500 transfer...
    [PAUSED] Action requires human supervisor approval!
    Approval ID: appr_99182371a2bf
    Expires At:  2026-10-13T20:30:00
    Human Supervisor reviewing via /approvals API...
    Supervisor Decision: APPROVED.
    [RESUMED] Tool executed successfully: transferred

[9] Verifying Immutable Hash-Chained Audit Ledger...
    Audit Chain Status: verified_intact
    Verified Records:   4
    Ledger Head Hash:   7e1a3b98c52d...

[10] Testing Anomaly Detection: Simulating Denial Burst on Sub-Agent...
    Burst of 5 denials submitted in sliding window.
    [ALERT TRIGGERED] Severity: critical, Action: suspend
    Verifying immediate kill-switch enforcement on Sub-Agent...
    [KILL SWITCH ACTIVE] Sub-Agent Execution Terminated: Terminated by ANUBIS Kill Switch.

======================================================================
  ANUBIS Zero-Trust Workflow Demo Completed Successfully!
======================================================================
```

---

## 🔥 The Trial of Fifty-One Flayed Souls: Test Suite (51/51 Passing)

ANUBIS undergoes mathematical validation across **51 unit and integration tests** verifying cryptographic challenges, replay rejection, monotonic delegation, tamper detection, multi-vector kill switches, and SDK abstractions:

```powershell
python -m pytest -v
```

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\kollu\Documents\PROJECTS\ANUBIS
collected 51 items

tests/test_approvals.py::test_approval_hold_and_resume_flow PASSED       [  1%]
tests/test_approvals.py::test_rejection_of_approval_request PASSED       [  3%]
tests/test_audit.py::test_agent_cryptographic_unique_id_created_at_registration PASSED [  5%]
tests/test_audit.py::test_audit_hash_chain_logged_on_gateway_calls PASSED [  7%]
tests/test_audit.py::test_audit_secret_redaction PASSED                  [  9%]
tests/test_audit.py::test_tamper_detection_on_altered_record PASSED      [ 11%]
tests/test_auth.py::test_jwks_endpoint PASSED                            [ 13%]
tests/test_auth.py::test_full_challenge_response_authentication PASSED   [ 15%]
tests/test_auth.py::test_auth_wrong_signature_fails PASSED               [ 17%]
tests/test_delegation.py::test_task_creation_and_lifecycle PASSED        [ 19%]
tests/test_delegation.py::test_token_exchange_scope_narrowing_and_act_chain PASSED [ 21%]
tests/test_delegation.py::test_privilege_escalation_attempt_strictly_denied PASSED [ 23%]
tests/test_delegation.py::test_multi_agent_workflow_simulation PASSED    [ 25%]
tests/test_delegation.py::test_cannot_delegate_to_revoked_or_suspended_agent PASSED [ 27%]
tests/test_detection.py::test_baseline_tracking_and_retrieval PASSED     [ 29%]
tests/test_detection.py::test_novel_tool_probe_alert PASSED              [ 31%]
tests/test_detection.py::test_denial_burst_automated_killswitch PASSED   [ 33%]
tests/test_detection.py::test_alert_update_lifecycle PASSED              [ 35%]
tests/test_gateway.py::test_gateway_mcp_tools_list PASSED                [ 37%]
tests/test_gateway.py::test_gateway_authorized_tool_call_and_credential_brokering PASSED [ 39%]
tests/test_gateway.py::test_gateway_unauthorized_tool_call_missing_scope PASSED [ 41%]
tests/test_gateway.py::test_gateway_argument_violation_triggers_approval PASSED [ 43%]
tests/test_gateway.py::test_gateway_dangerous_tool_denied PASSED         [ 45%]
tests/test_gateway.py::test_gateway_rejects_missing_and_invalid_token PASSED [ 47%]
tests/test_gateway.py::test_gateway_instant_kill_switch_revocation PASSED [ 49%]
tests/test_gateway.py::test_gateway_fail_closed_on_policy_outage PASSED  [ 50%]
tests/test_policy.py::test_policy_allow_read_tool PASSED                 [ 52%]
tests/test_policy.py::test_policy_deny_missing_scope PASSED              [ 54%]
tests/test_policy.py::test_policy_internal_vs_external_email PASSED      [ 56%]
tests/test_policy.py::test_policy_financial_transaction_threshold PASSED [ 58%]
tests/test_policy.py::test_policy_dangerous_tool_denied_for_low_tier PASSED [ 60%]
tests/test_policy.py::test_policy_registration_and_simulation_api PASSED [ 62%]
tests/test_registry.py::test_create_and_get_owner PASSED                 [ 64%]
tests/test_registry.py::test_register_agent_with_auto_keypair PASSED     [ 66%]
tests/test_registry.py::test_register_agent_with_custom_keypair PASSED   [ 68%]
tests/test_registry.py::test_update_agent_status_suspend_and_revoke PASSED [ 70%]
tests/test_revocation.py::test_kill_switch_by_agent_id PASSED            [ 72%]
tests/test_revocation.py::test_kill_switch_by_instance_id PASSED         [ 74%]
tests/test_revocation.py::test_kill_switch_by_token_jti PASSED           [ 76%]
tests/test_revocation.py::test_kill_switch_by_human_principal PASSED     [ 78%]
tests/test_sdk.py::test_sdk_registration_and_authentication PASSED       [ 80%]
tests/test_sdk.py::test_sdk_tool_invocation_and_credential_isolation PASSED [ 82%]
tests/test_sdk.py::test_sdk_delegation_and_monotonic_narrowing PASSED    [ 84%]
tests/test_sdk.py::test_sdk_human_approval_hold_and_resume PASSED        [ 86%]
tests/test_sdk.py::test_sdk_anomaly_detection_killswitch PASSED          [ 88%]
tests/test_tokens.py::test_valid_token_issuance_and_verification PASSED  [ 90%]
tests/test_tokens.py::test_expired_token_rejected PASSED                 [ 92%]
tests/test_tokens.py::test_tampered_token_payload_rejected PASSED        [ 94%]
tests/test_tokens.py::test_tampered_token_signature_rejected PASSED      [ 96%]
tests/test_tokens.py::test_replayed_challenge_rejected PASSED            [ 98%]
tests/test_tokens.py::test_suspended_and_revoked_agent_cannot_authenticate PASSED [100%]

======================== 51 passed in 1.22s ========================
```

---

## 🛠️ Summoning the Underworld (Quickstart)

### 1. Standalone Python Setup
```powershell
# Clone the necropolis
git clone https://github.com/i-mAshura/ANUBIS.git
cd ANUBIS

# Create virtual realm
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows
# source venv/bin/activate     # Linux / macOS

# Install sacred runes
pip install -r requirements.txt

# Awaken the ANUBIS Control Plane
uvicorn anubis.main:app --reload --port 8000
```

Access the shrines:
* 📜 **Swagger UI Altar:** `http://localhost:8000/docs`
* ⚖️ **Public JWKS Keys:** `http://localhost:8000/.well-known/jwks.json`
* 🩸 **System Health Check:** `http://localhost:8000/health`

### 2. Summon via Docker Compose
```bash
docker compose up -d
```
Spawns PostgreSQL, Redis, Open Policy Agent, and ANUBIS in a hardened, network-isolated container perimeter.

---

## ⚖️ The Sacred Creed

> *"He who steps through the gate must bear the mark of his maker.*  
> *His heart shall be weighed upon the feather of truth,*  
> *and should his intent tip into shadow,*  
> *the guillotine blade shall claim him before his hand strikes the stone."*

---

## 🩸 License
Crafted under the **Apache License 2.0**. See [LICENSE](LICENSE) for terms.  
Inscriptions, issues, and security advisories are welcome in the underworld hall.
