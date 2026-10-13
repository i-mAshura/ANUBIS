# 𓁢 A N U B I S
### *∮ The Obsidian Control Plane ∮ Cryptographic Necromancy, Zero-Trust IAM & Abyssal Surveillance for Autonomous AI Agents*

<p align="center">
  <img src="https://img.shields.io/badge/HELLFIRE-ACTIVE%20CONFLAGRATION-800000?style=for-the-badge&logo=ghostery&logoColor=red" alt="Hellfire Active" />
  <img src="https://img.shields.io/badge/JUDGMENT-FAIL--CLOSED%20GUILLOTINE-000000?style=for-the-badge&logo=shield&logoColor=crimson" alt="Guillotine Fail-Closed" />
  <img src="https://img.shields.io/badge/SCALES_OF_MAAT-ES256%20ECDSA%20P--256-4a0000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="ES256 ECDSA" />
  <img src="https://img.shields.io/badge/AUDIT_LEDGER-SHA--256%20HASH--CHAINED-1a0000?style=for-the-badge&logo=git&logoColor=darkred" alt="Hash-Chained Audit" />
  <img src="https://img.shields.io/badge/SOULS_WEIGHED-51%2F51%20TRIALS%20PASSED-330000?style=for-the-badge&logo=checkmarx&logoColor=lime" alt="51 Tests Passed" />
  <img src="https://img.shields.io/badge/LICENSE-APACHE_2.0-550000?style=for-the-badge" alt="License" />
</p>

```
          )      (        )     (         )      (       )
         (  )   ) \    ( /(   ( )\     ) ( /(   ( )\   ( /(
        ) \ /( ( ) )   )\()) )\(_)) ( /( )\())  )\_))  )\())
       ( ( )\()|()/(  ((_)\ ((_)_  )\()|(_)\ ((_)_ ((_)\
       )\ ((_)\ )(_))  _((_) | _ )((_)\ _((_) | _ ) /  _/
      ((_)| |(_)((_)_  | \| | | _ \ | || | | _ \ \ \ \ \
                                                         
 ░▒▓█▓▒░ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ░▒▓█▓▒░
 ▓▓▓▓▓▓▓ ┌────────────────────────────────────────┐ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │   ☠   𓁢   A N U B I S   𓁢   ☠         │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │                                        │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │  ∀ agent a :  Pr[ pass | impure ] ≡ 0  │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │                                        │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │   ABANDON ALL HOPE, YE WHO ENTER       │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ │   WITHOUT A VALID SIGNATURE            │ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓ └────────────────────────────────────────┘ ▓▓▓▓▓▓▓
 ▓▓▓▓▓▓▓       ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║       ▓▓▓▓▓▓▓
 ░▒▓█▓▒░  ~ ~ ~ ~ ~ THE LAKE OF FIRE ~ ~ ~ ~ ~  ░▒▓█▓▒░
```

```
                                      /\
                                     /  \
                                    / /\ \
                                   / /  \ \
              __________________  / /    \ \  __________________
             |                  |/ /      \ \|                  |
             |    ( ◉ )  ( ◉ )     [ THE SCALES ]    ( ◉ )  ( ◉ )  |
             |        \/            ⚖  ⚖  ⚖            \/        |
             |__________________________________________________|
                  [ THE HEART OF THE AGENT ]   [ THE FEATHER OF TRUTH ]
                                     │
                                     ▼
              ∥ heart(a) ∥  ≤  ∥ feather ∥   ⟹   PASS
              ∥ heart(a) ∥  >  ∥ feather ∥   ⟹   AMMIT DEVOURS
```

> *"EVERY AGENT IS WEIGHED BEFORE IT PASSES, AND IN THE UNDERWORLD, THE RECORD NEVER LIES."*

---

## 🩸 Prologue: The Horrific Reality of AI Autonomy

In the mortal plane of software, unbaptized autonomous agents roam like fleshless wraiths. They are handed almighty static master credentials; they burrow through production databases; they swallow prompt-injected incantations whole; and they spawn recursive swarms of ungoverned sub-demons. When injection strikes, the blast radius is absolute, **because the agent has no immutable birthmark, no cryptographic boundary, and no judge.**

**ANUBIS** is the black-obsidian control plane at the mouth of the abyss. Named for the jackal-headed god who weighs the heart against the Feather of Truth:

> ⚖️ **If the token is unblemished, the lineage pure, and the scope monotonically restricted: the agent may pass.**
> ⚔️ **If the heart is heavy with forged scopes, stolen tokens, anomalous tool probing, or prompt injection: the guillotine drops. Execution is severed in milliseconds, the soul is hurled to Ammit, and the damnation is branded into a ledger that cannot be quietly rewritten.**

---

## ☠️ The Adversary: Threat Model of the Damned

Let $\mathcal{A}$ be a probabilistic polynomial-time adversary. ANUBIS assumes $\mathcal{A}$ may:

| Rune | Capability of the Adversary | Counter-Ritual |
|:---:|:---|:---|
| ☠ α | Fully control an agent's prompts (**prompt injection**) | Authority is bound to the token, not the prompt (Pillars III, IV) |
| ☠ β | Steal or replay a bearer token or a challenge | Single-use nonce; 900 s token life; JTI revocation (II, VII) |
| ☠ γ | Spawn sub-agents to launder privilege | Monotonic scope collapse + `act` lineage (III) |
| ☠ δ | Induce policy timeouts, crashes, malformed input | Fail-closed gate: default **DENY** (IV) |
| ☠ ε | Exfiltrate downstream secrets through tool output | Brokered credentials + response scrubbing (V) |
| ☠ ζ | Edit the audit trail after the fact | Hash-chained, tamper-evident ledger (VI) |
| ☠ η | Probe tools and burst-retry until something gives | Sliding-window detection + 5-vector kill switch (VII) |

---

## 🏛️ The Infernal Architecture: Bifurcation of Planes

ANUBIS enforces a hard separation between the ethereal plane of governance (**Control Plane**) and the iron gates of execution (**Data Plane**):

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

## 🔥 The Master Equation of Judgment

Every request $r$ that reaches the Obsidian Gate is reduced to a single verdict. Let $\sigma_r$ be its token, $S_{\mathrm{req}}(r)$ the scope the tool demands, $\pi$ the OPA policy decision, and $\tau$ the policy latency:

$$
\mathrm{Verdict}(r)=
\begin{cases}
\mathsf{ALLOW} & \text{if } \;
\underbrace{\mathrm{Valid}(\sigma_r)}_{\text{signature, } \mathrm{exp}}
\;\wedge\;
\underbrace{\neg\,\mathrm{Revoked}(r)}_{\text{5-vector }\mathbf{K}}
\;\wedge\;
\underbrace{S_{\mathrm{req}}(r)\subseteq S_{\sigma_r}}_{\text{scope}}
\;\wedge\;
\underbrace{\pi(r)=\mathsf{allow}}_{\text{Ma'at}}
\;\wedge\;
\underbrace{\tau\le 50\,\mathrm{ms}}_{\text{no stalling}} \\[6pt]
\mathsf{HOLD} & \text{if } \pi(r)=\mathsf{hold} \quad(\text{await human mercy}) \\[6pt]
\mathsf{DENY} & \text{otherwise (including every error, timeout, and malformed byte)}
\end{cases}
$$

`ALLOW` is the **conjunction of five positively observed facts**. Absence of evidence is never permission.

---

## ⚔️ The Seven Circles of Eternal Retribution

```
   ╔══ CIRCLE I   ══ IDENTITY ══════  agt_ ‖ Trunc₂₄( SHA-256( DER(K_pub) ) )
   ║
   ╠══ CIRCLE II  ══ PROOF ═════════  σ = Sign_K_priv( N ),  N ←R {0,1}^256
   ║
   ╠══ CIRCLE III ══ DELEGATION ════  S_child ⊆ S_parent   (a meet-semilattice)
   ║
   ╠══ CIRCLE IV  ══ THE GATE ══════  Pr[ exec | fault ] ≡ 0
   ║
   ╠══ CIRCLE V   ══ SECRETS ═══════  Scrub( raw, V ) ∩ V = ∅
   ║
   ╠══ CIRCLE VI  ══ THE LEDGER ════  Hᵢ = SHA-256( ⟨Eᵢ⟩ ‖ Hᵢ₋₁ )
   ║
   ╚══ CIRCLE VII ══ THE SCOURGE ═══  D(a, 60s) ≥ 5  ⟹  SUSPEND ∧ REVOKE
```

---

### 🔥 Circle I · 𓋹 The Crypt of Souls: Atomic Cryptographic Identity

No nameless phantom crosses the River of Fire. At registration (`POST /agents`) an agent cannot pick its own name. The name is *derived*, atomically, from its public key on NIST P-256:

$$E(\mathbb{F}_p):\; y^2 \equiv x^3 - 3x + b \pmod p \qquad (\text{NIST P-256 / secp256r1})$$

$$\mathbf{ID}(a) \;=\; \texttt{agt\_}\;\Vert\;\mathrm{Hex}\big(\mathrm{SHA256}(\mathrm{DER}(K_{\mathrm{pub}}))\big)\big[0{:}24\big]$$

> **Definition I.1 (Soul Space).** The suffix keeps 24 hex digits, i.e. $24 \times 4 = 96$ bits, so $|\mathcal{I}| = 2^{96}$.

> **Theorem I.1 (Soul Uniqueness).** For $q$ registered agents with independently generated keys, the probability that any two share an identity satisfies
> $$\Pr[\text{collision}] \;\le\; \frac{q(q-1)}{2\cdot 2^{96}} \;<\; \frac{q^2}{2^{97}}.$$
> *Illustration:* for $q = 2^{30}\approx 10^9$ agents, $\Pr[\text{collision}] < 2^{-37}$.

> **Theorem I.2 (Key Non-Possession).** The private key $K_{\mathrm{priv}}$ is generated inside the agent's memory boundary. ANUBIS stores only $K_{\mathrm{pub}}$ and therefore **cannot** impersonate an agent, and a full database compromise yields no signing capability.

---

### 🔥 Circle II · 𓇯 The Weighing of the Heart: Challenge-Response Ritual

Static bearer secrets are an abomination. To act, an agent must prove it holds the key:

1. **The Nonce Incantation.** The agent requests a fresh unpredictable challenge:
   $$\mathcal{N}\;\xleftarrow{\;\mathrm{R}\;}\;\{0,1\}^{256},\qquad \mathrm{TTL}(\mathcal{N}) \le 300\ \mathrm{s}$$
2. **The Signature of Flesh.** The agent signs it:
   $$\sigma = \mathrm{Sign}_{K_{\mathrm{priv}}}(\mathcal{N})$$
3. **The Issuance of Ephemeral Life.** If $\mathrm{Verify}_{K_{\mathrm{pub}}}(\mathcal{N},\sigma)=1$ the nonce is **burned** and an instance-bound ES256 JWT is minted:
   $$\mathcal{T}=\mathrm{Sign}_{\mathrm{ANUBIS}}\big(\mathrm{sub}=\mathbf{ID}(a),\ \mathrm{jti}=\mu,\ \mathrm{exp}=t_{\mathrm{now}}+900\,\mathrm{s},\ \mathrm{scope}=\mathcal{S}\big)$$

> **Lemma II.1 (Replay Immunity).** A nonce is consumed on first successful verification. A second presentation of the same $(\mathcal{N},\sigma)$ is rejected, and guessing a live nonce succeeds with probability $2^{-256}$ per attempt.

> **Lemma II.2 (Bounded Exposure).** A stolen token is useful for at most $900\,\mathrm{s}$, and sooner if its JTI or agent is placed in $\mathbf{K}$ (Circle VII).

*Security note:* ECDSA P-256 offers roughly 128-bit classical security. It is not post-quantum.

---

### 🔥 Circle III · 𓍝 The Scales of Ma'at: Monotonic Scope Collapse & Lineage

When an agent delegates (`POST /auth/exchange`) it can **never** grant more than it holds. Scopes live in the power-set lattice $(\mathcal{P}(\Sigma), \subseteq, \cap)$:

$$\mathcal{S}_{\mathrm{child}}\subseteq\mathcal{S}_{\mathrm{parent}}\quad\Longleftrightarrow\quad\forall s\in\mathcal{S}_{\mathrm{child}},\; s\in\mathcal{S}_{\mathrm{parent}}$$

If $\exists\, s\in\mathcal{S}_{\mathrm{child}}$ with $s\notin\mathcal{S}_{\mathrm{parent}}$, the exchange is refused with `HTTP 403 Forbidden`.

> **Theorem III.1 (No Privilege Escalation).** For any delegation chain $a_0\to a_1\to\dots\to a_k$,
> $$\mathcal{S}_k\subseteq\mathcal{S}_{k-1}\subseteq\dots\subseteq\mathcal{S}_0\qquad\text{and}\qquad |\mathcal{S}_k|\le|\mathcal{S}_{k-1}|\le\dots\le|\mathcal{S}_0|.$$
> *Proof.* Each exchange enforces $\mathcal{S}_i\subseteq\mathcal{S}_{i-1}$. Induction on $k$ and transitivity of $\subseteq$ give $\mathcal{S}_k\subseteq\mathcal{S}_0$. $\blacksquare$

**The Ancestral Actor Chain (`act`).** The lineage vector is appended into every delegated token:

$$\mathbf{act}_k=\big[\mathbf{ID}(a_0),\ \mathbf{ID}(a_1),\ \dots,\ \mathbf{ID}(a_k)\big],\qquad |\mathbf{act}_k|=k+1$$

Downstream tools inspect not just the caller, but its entire bloodline. A sub-demon can never outrank the demon that spawned it.

---

### 🔥 Circle IV · 𓆣 The Obsidian Guillotine: Fail-Closed Gateway Invariant

Every Model Context Protocol tool call (`POST /mcp/{server}`) passes under the Obsidian Gate.

$$\mathbb{P}\big(\text{Tool Execution}\ \big|\ \text{Policy Timeout}\ \lor\ \text{Network Outage}\ \lor\ \text{Rego Error}\ \lor\ \text{Malformed Signature}\big)\;\equiv\;0$$

> **Theorem IV.1 (Default Damnation).** Let $F$ be any fault event (timeout $\tau>50\,\mathrm{ms}$, policy compile failure, I/O error, invalid signature). Since $\mathsf{ALLOW}$ requires *every* conjunct of the Master Equation to be positively observed, and a fault prevents at least one from being observed, $\mathrm{Verdict}\ne\mathsf{ALLOW}$ under $F$.
> *Implementation assumption:* every code path out of a fault terminates in `DENY`. This is exercised by `test_gateway_fail_closed_on_policy_outage`.

The default state of the universe is **DENY**.

---

### 🔥 Circle V · 𓋖 The Canopic Jars of Secrets: Downstream Credential Isolation

Agents never touch master credentials, database passwords, or third-party keys.

1. **Vault Isolation.** Downstream secrets live only in ANUBIS's encrypted vault.
2. **Credential Brokering.** ANUBIS injects secrets into downstream calls on the agent's behalf.
3. **Mutilation & Redaction.** Responses are scrubbed before they return:

$$\mathrm{Resp}_{\mathrm{san}}=\mathrm{ScrubSecrets}\big(\mathrm{Resp}_{\mathrm{raw}},\ \mathcal{V}_{\mathrm{secrets}}\big)\qquad\text{s.t.}\quad\forall v\in\mathcal{V}_{\mathrm{secrets}}:\ v\notin\mathrm{Substr}(\mathrm{Resp}_{\mathrm{san}})$$

*Scope of the guarantee:* it holds for registered secret values and configured patterns. Re-encoded forms (base64, split across fields) are outside the guarantee unless a pattern covers them.

---

### 🔥 Circle VI · 𓉣 The Book of the Dead: Hash-Chained Necrology

Every attempt, argument payload, verdict, latency, and error is inscribed into an append-only ledger:

$$H_0 = 0^{256},\qquad H_i=\mathrm{SHA256}\Big(\mathrm{CanonicalJSON}(\mathcal{E}_i)\ \Vert\ H_{i-1}\Big)\quad\forall\, i\ge 1$$

> **Theorem VI.1 (Tamper Evidence).** If record $\mathcal{E}_k$ is altered to $\mathcal{E}_k'\neq\mathcal{E}_k$, then unless $\mathcal{A}$ finds a SHA-256 collision (cost $\approx 2^{128}$ by the birthday bound), the recomputed $H_k'\ne H_k$, and every $H_j$ for $j\ge k$ mismatches:
> $$\exists k:\ H_k\neq\mathrm{SHA256}\big(\mathcal{E}_k\Vert H_{k-1}\big)\ \Longrightarrow\ \text{TAMPER ALARM}$$
> `GET /audit/verify` walks the chain in $O(n)$.

*Operational note:* an attacker who can rewrite **every** record from $k$ onward can recompute a consistent chain. Anchor the head hash $H_n$ somewhere the attacker cannot reach (WORM storage, a separate trust domain, or a periodic signed checkpoint) to make this detectable.

---

### 🔥 Circle VII · 𓌃 The Scourge of Ammit: Denial Bursts & the 5-Vector Kill Switch

The Detection Engine watches a sliding window for every living soul:

$$\mathcal{D}(a,\Delta t)=\sum_{t_i\in[\,t_{\mathrm{now}}-\Delta t,\ t_{\mathrm{now}}\,]}\mathbb{1}\Big[\mathrm{Verdict}(a,t_i)=\mathsf{DENY}\Big]$$

$$\mathcal{D}(a,\,60\,\mathrm{s})\ \ge\ 5\ \Longrightarrow\ \mathrm{Action}(a)\leftarrow\textbf{CRITICAL SUSPENSION}$$

The agent is suspended in the registry and injected into the **Kill Switch Manifold** $\mathbf{K}=(K_{\mathcal{A}},K_{\mathcal{I}},K_{\mathcal{T}},K_{\mathcal{J}},K_{\mathcal{P}})$, one blacklist per vector. A request $r$ carrying agent $a$, instance $i$, task $t$, token id $\mu$, principal $p$ is revoked if **any** coordinate matches:

$$\mathrm{Revoked}(r)\;=\;[a\in K_{\mathcal{A}}]\ \lor\ [i\in K_{\mathcal{I}}]\ \lor\ [t\in K_{\mathcal{T}}]\ \lor\ [\mu\in K_{\mathcal{J}}]\ \lor\ [p\in K_{\mathcal{P}}]$$

```text
  Revocation Manifold (example):
  {
    Agent ID:         agt_ca51d8ac48ed9d2f28ff05c5  (terminates entire agent lineage)
    Instance ID:      inst-sec-1                    (terminates a specific container)
    Task ID:          task-detection-test           (terminates the task tree)
    Token JTI:        c82a19b0-4f81-49b2-9981       (terminates a specific JWT)
    Human Principal:  sec_admin                     (terminates a compromised human)
  }
```

Matching calls are obliterated with `HTTP 403 Forbidden` via fast key-value lookups.

---

## 📜 The Nine Circles of the API: Full Blueprint

```http
### ============ CIRCLE I · THE CRYPT OF SOULS (REGISTRY) ============
POST   /owners                          # Inscribe accountable mortal master or team
GET    /owners                          # Enumerate all registered mortal owners
GET    /owners/{id}                     # Inspect specific owner details
POST   /agents                          # Inscribe agent (Atomic ES256 P-256 ID derivation)
GET    /agents                          # Enumerate agents (filter: active, suspended, revoked)
GET    /agents/{id}                     # Inspect agent identity & stored public key
PATCH  /agents/{id}                     # Mutate status (active -> suspended -> revoked)
POST   /agents/{id}/instances           # Bind ephemeral runtime execution container

### ============ CIRCLE II · THE TRIAL OF PROOF (AUTH & TOKENS) ============
POST   /auth/challenge                  # Generate cryptographically secure nonce challenge
POST   /auth/token                      # Verify ECDSA signature and mint task-scoped ES256 JWT
POST   /auth/exchange                   # Monotonic token exchange for delegated sub-agents
POST   /auth/keypair                    # Helper ritual: forge an ECDSA P-256 keypair
GET    /.well-known/jwks.json           # RFC 7517 JSON Web Key Set of ANUBIS signing keys

### ============ CIRCLE III · THE SCALES OF MAAT (POLICY ENGINE) ============
POST   /policies                        # Register declarative OPA/Rego governance rule
GET    /policies                        # List active policies in the underworld
POST   /policies/simulate               # Dry-run policy evaluation against hypothetical action

### ============ CIRCLE IV · THE OBSIDIAN GATE (DATA PLANE MCP PROXY) ============
POST   /tools                           # Register downstream tool, risk level & brokered secrets
GET    /tools                           # Enumerate registered tools and JSON argument schemas
POST   /mcp/{server}                    # Intercepted JSON-RPC 2.0 tool execution gateway

### ============ CIRCLE V · THE BOOK OF THE DEAD (SURVEILLANCE & AUDIT) ============
GET    /audit                           # Retrieve immutable audit events (agent, tool, outcome)
GET    /audit/verify                    # Mathematical SHA-256 hash-chain tamper detection check

### ============ CIRCLE VI · TASKS & DELEGATION HIERARCHIES ============
POST   /tasks                           # Create scoped task container for agent workflows
GET    /tasks                           # Enumerate tasks and subtask lineage
GET    /tasks/{id}                      # Inspect specific task status and delegation chain

### ============ CIRCLE VII · PLEAS FOR MERCY (HUMAN APPROVALS) ============
GET    /approvals                       # Enumerate pending approval requests
GET    /approvals/{id}                  # Inspect specific approval parameters
POST   /approvals/{id}/decision         # Render verdict: 'approved' or 'rejected'

### ============ CIRCLE VIII · THE FIVE-VECTOR KILL SWITCH ============
POST   /revocations                     # Blacklist by agent, instance, task, jti, or principal
GET    /revocations                     # Enumerate active damnation entries
POST   /revocations/check               # Microsecond revocation check query
DELETE /revocations/{id}                # Pardon/lift revocation entry

### ============ CIRCLE IX · THE SCOURGE OF AMMIT (ANOMALY DETECTION) ============
GET    /alerts                          # Query detection alerts (denial_burst, novel_tool_probe)
PATCH  /alerts/{id}                     # Triage alert: active -> acknowledged -> resolved
GET    /baselines/{agent_id}            # Inspect learned behavioral profile & call history
```

---

## 🐍 The Serpent's Grasp: Python SDK (`anubis.sdk`)

ANUBIS ships with a zero-dependency Python SDK to govern any LLM agent framework (LangChain, AutoGen, CrewAI, or direct OpenAI/Anthropic tool runners).

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

## 🕯️ The Ritual of Verification: Live Multi-Agent Workflow Demo

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

## 💀 The Trial of Fifty-One Flayed Souls: Test Suite (51/51)

$$\forall\, i\in\{1,\dots,51\}:\ \mathrm{Test}_i=\mathsf{PASSED}\ \Longrightarrow\ \textstyle\sum_{i=1}^{51}\mathbb{1}[\mathrm{Test}_i]=51$$

Coverage: cryptographic challenges, replay rejection, monotonic delegation, tamper detection, multi-vector kill switches, and SDK abstractions.

```powershell
python -m pytest -v
```

```text
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\...\ANUBIS
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

## 🛠️ Descending Into the Underworld (Quickstart)

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

```
   ░▒▓█  🔥  🔥  🔥  🔥  🔥  🔥  🔥  🔥  🔥  🔥  🔥  █▓▒░
```

> *"He who steps through the gate must bear the mark of his maker.*
> *His heart shall be weighed upon the feather of truth,*
> *and should his intent tip into shadow,*
> *the guillotine blade shall claim him before his hand strikes the stone."*

$$\boxed{\ \forall a:\ \ \mathrm{Pass}(a)\iff\mathrm{Valid}\wedge\neg\mathrm{Revoked}\wedge\mathcal{S}_{\mathrm{req}}\subseteq\mathcal{S}\wedge\pi=\mathsf{allow}\ }\qquad\blacksquare$$

---

## 🩸 License
Crafted under the **Apache License 2.0**. See [LICENSE](LICENSE) for terms.
Inscriptions, issues, and security advisories are welcome in the underworld hall.
