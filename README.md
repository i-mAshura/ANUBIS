# 𓁢 A N U B I S
### *Identity, Zero-Trust IAM & Cryptographic Surveillance for AI Agents*

<p align="center">
  <img src="https://img.shields.io/badge/HELLFIRE-ACTIVE-990000?style=for-the-badge&logo=ghostery&logoColor=white" alt="Hellfire Active" />
  <img src="https://img.shields.io/badge/JUDGMENT-FAIL--CLOSED-black?style=for-the-badge&logo=shield&logoColor=red" alt="Judgment Fail-Closed" />
  <img src="https://img.shields.io/badge/SCALES_OF_MAAT-ES256%20ECDSA-800020?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="ES256" />
  <img src="https://img.shields.io/badge/IMMUTABLE-HASH--CHAINED-330000?style=for-the-badge&logo=git&logoColor=white" alt="Hash Chained" />
  <img src="https://img.shields.io/badge/LICENSE-APACHE_2.0-550000?style=for-the-badge" alt="License" />
</p>

```
                       .---.
                      /     \
                     | () () |       "EVERY AGENT IS WEIGHED
                      \  _  /         BEFORE IT PASSES,
                       `---'          AND THE RECORD NEVER LIES."
                      /| | |\
                     / |_|_| \
    ⚔️═══════════════[ ANUBIS ]════════════════════════════════════════⚔️
    Agent Namespace, Unified Boundaries, Identity & Surveillance
```

---

## ⚖️ The Decrees of the Underworld

In the mortal realm of software, autonomous AI agents roam unchecked. They wield static master API keys, touch production vaults, and summon sub-agents in chaotic cascades. When an agent is corrupted by prompt injection, its blast radius is absolute—because **it has no identity, no boundary, and no judge.**

**ANUBIS** is the obsidian gatekeeper that stands between autonomous agents and the realms of data and tools. Like the jackal-headed god who places the mortal heart upon the Golden Scales of Ma'at against the Feather of Truth:

* If an agent's token is untampered, its purpose pure, and its scope narrow: **It may pass.**
* If its heart is heavy with stolen tokens, forged delegation, prompt injection, or forbidden tool calls: **Anubis drops the blade. Access is denied, and the breach is etched forever into the immutable ledgers of the underworld.**

---

## 🏛️ The Infernal Architecture: Two Planes of Judgment

ANUBIS strictly bifurcates the ethereal realm (**Control Plane**) from the iron gates of execution (**Data Plane**):

```
                        [ MORTAL MASTERS & ADMINS ]
                                     │
                             [ THE HIGH ALTAR ]
                                (Dashboard)
                                     │
                                     ▼
   ╔═══════════════════════════════════════════════════════════════════╗
   ║                   THE ANUBIS CONTROL PLANE                        ║
   ║                                                                   ║
   ║  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  ║
   ║  │ AGENT REGISTRY  │   │  AUTH & TOKENS  │   │  POLICY ENGINE  │  ║
   ║  │ (The Roll of    │   │ (Challenge /    │   │ (The Scales /   │  ║
   ║  │  Living Souls)  │   │  Ephemeral JWT) │   │  OPA Rego)      │  ║
   ║  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘  ║
   ║           │                     │                     │           ║
   ║  ┌────────┴────────┐   ┌────────┴────────┐            │           ║
   ║  │ APPROVAL SERVICE│   │ DETECTION ENGINE│            │           ║
   ║  │ (Plea for Mercy)│   │ (Curse / Anomaly│            │           ║
   ║  └─────────────────┘   └─────────────────┘            │           ║
   ║           │                     │                     │           ║
   ║           ▼                     ▼                     ▼           ║
   ║  ┌─────────────────────────────────────────────────────────────┐  ║
   ║  │ PostgreSQL (Relational Core)  │ Redis (Instant Damnation)   │  ║
   ║  └─────────────────────────────────────────────────────────────┘  ║
   ╚═══════════════════════════════════════════════════════════════════╝
                                     ▲
                            VERDICT / JWKS / REVOCATION
                                     │
 ┌───────────────┐                   ▼                   ┌────────────────┐
 │ AUTONOMOUS    │       ┌───────────────────────┐       │ DOWNSTREAM     │
 │ AI AGENT      ├──────►│   THE OBSIDIAN GATE   ├──────►│ TOOLS, MCP     │
 │ (The Pilgrim) │       │   (MCP Proxy / Data   │       │ SERVERS, APIS  │
 └───────────────┘       │    Plane Gateway)     │       └────────────────┘
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

## 🔥 The Pillars of Retribution

### 1. 𓋹 The Mark of Souls (Agent Cryptographic Identity)
No nameless phantom may invoke a tool. Every agent must register with an accountable mortal owner, declare its environment and risk tier, and be bound to an asymmetric cryptographic keypair (**ECDSA P-256 / ES256**). The private key never leaves the agent runtime; the public key is inscribed in the registry.

### 2. 𓇯 The Challenge Ritual (Zero-Trust Authentication)
Static tokens are an abomination. When an agent demands audience:
1. It requests a one-time cryptographic challenge nonce from the underworld: `POST /auth/challenge`.
2. It signs the challenge with its private key in the shadows.
3. It presents the signature to `POST /auth/token`.
4. If the signature rings true, ANUBIS mints an ephemeral, instance-bound JWT valid for mere minutes. Replay attacks are consumed by fire instantly.

### 3. 𓍝 The Scales of Ma'at (Monotonic Delegation Narrowing)
When a high-tier agent delegates to a subservient sub-agent, the lineage is sealed into the cryptographic `act` claim:
$$\text{Scope}(\text{Sub-Agent}) \subseteq \text{Scope}(\text{Parent Agent})$$
Privilege escalation is impossible. A child agent can never claim more power than the spirit that spawned it.

### 4. 𓆣 The Obsidian Gate (Fail-Closed MCP Gateway)
The agent never touches raw credentials for target databases, APIs, or MCP servers. All calls flow through the ANUBIS Gateway. If the policy engine is unreachable, or the token signature is corrupt: **the gate shuts, failing closed.**

### 5. 𓉣 The Book of the Dead (Hash-Chained Audit Trail)
Every tool call, argument, timestamp, and verdict is etched into an append-only, cryptographic hash-chained ledger:
$$\text{Hash}_n = \mathcal{H}(\text{Record}_n \parallel \text{Hash}_{n-1})$$
Any mortal or rogue process that alters or deletes a record breaks the chain, immediately flagged by `GET /audit/verify`.

### 6. 𓋒 Instant Damnation (The Redis Kill Switch)
When an agent is corrupted, goes rogue, or exhibits abnormal exfiltration bursts, the executioner drops the axe. A single call to `PATCH /agents/{id}` purges the agent and blacklists its tokens in Redis. Subsequent tool requests are crushed in milliseconds.

---

## ⚔️ The Threat Model Matrix

| # | Threat | Underworld Description | ANUBIS Retribution |
|:---:|---|---|---|
| **I** | **Credential Theft** | Leaked static keys passed through untrusted hands | Ephemeral, instance-bound JWTs (5–15 min TTL) verified against ECDSA keypairs. |
| **II** | **Confused Deputy** | Agent tricked into serving a foreign master | Mandatory `act` delegation chains and `on_behalf_of` human scoping. |
| **III** | **Privilege Escalation** | A sub-demon demanding more wrath than its master | Strict monotonic narrowing: child scope must be a subset of parent scope. |
| **IV** | **Prompt Injection** | Injected text coercing dangerous tool execution | Rego policies inspect tool names & arguments; high-risk actions locked behind human approval. |
| **V** | **Data Exfiltration** | Voracious bulk queries draining the vaults | Hard rate limits, strict destination allowlists, and volume anomaly tripping. |
| **VI** | **Rogue / Forgotten Agents** | Unchecked spirits lingering in production | Mandatory mortal owner, hard expiration dates (`expires_at`), and status auditing. |
| **VII** | **Log Tampering** | Intruders trying to erase their footsteps | Cryptographic hash-chained records ($\text{Hash}_n$). The record never lies. |
| **VIII**| **Token Replay** | Hijacking an intercepted bearer token | Unique token IDs (`jti`), single-use challenges, and runtime instance binding. |

---

## ⚡ The Grimoire of Endpoints (API Surface v1)

```http
# --- THE ROLL OF SOULS (REGISTRY) ---
POST   /owners                   # Register accountable mortal / team
GET    /owners                   # List registered owners
POST   /agents                   # Register agent (auto-generates ES256 keypair if needed)
GET    /agents                   # List agents (filter by: active, suspended, revoked)
GET    /agents/{id}              # Inspect agent identity & stored public key
PATCH  /agents/{id}              # Update status (active -> suspended -> revoked)
POST   /agents/{id}/instances    # Bind runtime execution instance

# --- THE TRIAL OF PROOF (AUTH & TOKENS) ---
POST   /auth/challenge           # Generate time-bounded cryptographically secure nonce
POST   /auth/token               # Verify ECDSA signature and issue task-scoped JWT
POST   /auth/keypair             # Helper ritual: forge an ECDSA P-256 keypair
GET    /.well-known/jwks.json    # Public JWKS of the underworld signing authority

# --- THE OBSIDIAN GATE (DATA PLANE) ---
POST   /mcp/{server}             # Proxied Model Context Protocol tool execution
GET    /audit/verify             # Cryptographic verification of the hash chain
```

---

## 🛠️ Summoning the Underworld (Quickstart)

### 1. Prerequisites
* **Python 3.11+**
* **Docker & Docker Compose** (Optional, for full stack with PostgreSQL, Redis & OPA)

### 2. Ignition
```powershell
# Clone the underworld repository
git clone https://github.com/i-mAshura/ANUBIS.git
cd ANUBIS

# Create virtual realm
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows
# source venv/bin/activate     # On Linux / macOS

# Install sacred runes
pip install -r requirements.txt

# Awaken the ANUBIS modular monolith
uvicorn anubis.main:app --reload --port 8000
```

The sacred scrolls will be available in your browser at:
* 📜 **Altar of Documentation (Swagger UI):** `http://localhost:8000/docs`
* ⚖️ **The Scales of Public Keys (JWKS):** `http://localhost:8000/.well-known/jwks.json`

### 3. Or Summon with Docker Compose
```bash
docker compose up -d
```
Spawns PostgreSQL, Redis, OPA, and the ANUBIS API in an isolated containerized perimeter.

---

## 🐍 The Serpent's Grasp: Python SDK & Autonomous Agent Client

ANUBIS provides a first-class Python SDK (`anubis.sdk`) designed for plug-and-play zero-trust governance across LLM agents and multi-agent frameworks (LangChain, AutoGen, CrewAI):

```python
from anubis.sdk import AnubisAgent, AnubisClient

# 1. Initialize client & register agent with local ECDSA P-256 keys
client = AnubisClient(base_url="http://localhost:8000")
agent = AnubisAgent(
    name="Orchestrator-Prime",
    owner_id="own_99182",
    purpose="Autonomous Financial Reconciliation",
    risk_tier="medium",
    capabilities=["tools:read", "tools:finance"],
    client=client
)
# Authenticates via cryptographic challenge-response
agent.bootstrap(scope=["tools:read", "tools:finance"])

# 2. Invoke MCP Tool (mediated by OPA policy, credentials brokered securely)
result = agent.execute_tool(
    server="corp-db",
    tool_name="read_records",
    arguments={"table": "quarterly_reports"}
)

# 3. Spawn Sub-Agent with Monotonic Scope Narrowing & 'act' Lineage
sub_agent = agent.spawn_subagent(
    name="Worker-Sub",
    purpose="Data extraction",
    task_intent="Extract quarterly numbers",
    delegated_scope=["tools:read"]  # Monotonically narrowed: cannot transfer funds
)
```

### 🚀 Run the Complete End-to-End Autonomous Agent Demo:
```powershell
python examples/autonomous_research_workflow.py
```
This runnable script walks through:
* Asymmetric keypair generation & atomic ID derivation (`agt_<hash>`)
* Challenge-response authentication & token acquisition
* Permitted tool execution with downstream secret redaction
* Sub-agent spawning with monotonic scope narrowing
* Privilege escalation rejection (fail-closed)
* Human supervisor approval hold-and-resume workflow
* Cryptographic hash-chain audit ledger verification
* Anomaly detection denial burst triggering automated kill-switch retribution!

---

## 🧪 The Trials of Fire (Test Suite)

Run the automated test suite verifying all 7 phases (identity, challenge-response, policy evaluation, gateway MCP mediation, hash-chained audit ledger, delegation exchange, human approvals, multi-dimensional kill switch, anomaly detection, and Python SDK):

```powershell
python -m pytest -v
```

```text
============================= test session starts =============================
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

## 📜 The Sacred Creed

> *"He who steps through the gate must bear the mark of his maker.*
> *His words shall be measured upon the feather,*
> *and should his intent tip into shadow,*
> *the fire shall claim him before his hand strikes the stone."*

---

## ⚖️ License

Crafted under the **Apache License 2.0**. See [LICENSE](LICENSE) for terms.
Contributions, issues, and security advisories are welcome in the underworld hall.
