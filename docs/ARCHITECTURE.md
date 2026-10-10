# ANUBIS Architecture Blueprint

## Architectural Overview
ANUBIS is split cleanly into two planes:
1. **Control Plane:** Manages agent identities, key registration, human ownership, issuance of short-lived tokens, policy authoring, approvals, and anomaly detection.
2. **Data Plane (Enforcement Point / Gateway):** An ultra-fast, fail-closed mediation gateway (MCP proxy and HTTP reverse proxy) that inspects every incoming tool call, evaluates policies against OPA, applies rate limits, redacts credentials, and emits tamper-evident audit records.

```
+-----------------------------------------------------------------------------+
|                                CONTROL PLANE                                |
|                                                                             |
|  +--------------+    +--------------+    +--------------+   +------------+  |
|  | Agent        |    | Auth &       |    | Policy       |   | Approval   |  |
|  | Registry     |    | Token Engine |    | Engine (OPA) |   | Engine     |  |
|  +-------+------+    +-------+------+    +-------+------+   +-----+------+  |
|          |                   |                   |                |         |
|          +-------------------+---------+---------+----------------+         |
|                                        |                                    |
|                      +-----------------+------------------+                 |
|                      |  PostgreSQL (Relational Store)     |                 |
|                      |  Redis (Revocations / Blacklist)   |                 |
|                      +------------------------------------+                 |
+-----------------------------------------------------------------------------+
                                         |
                                         | Cache Sync / JWKS / Policies
                                         v
+-----------------------------------------------------------------------------+
|                        DATA PLANE (ENFORCEMENT GATEWAY)                     |
|                                                                             |
|   Agent ---> [ Token Validation & Scope Check ] ---> [ OPA Policy Check ]   |
|                            |                                      |         |
|                            v                                      v         |
|                 [ Rate Limiting & Revocation ]        [ Credential Broker ] |
|                            |                                      |         |
|                            v                                      v         |
|                     [ Hash-Chained Audit Trail ]       ---> [ Target Tools ]|
+-----------------------------------------------------------------------------+
```

## Modular Monolith Structure
In v1, ANUBIS is built as a clean modular monolith using FastAPI. This avoids unnecessary distributed overhead, enables ultra-low latency enforcement, and simplifies deployment.

Modules:
- `anubis.services.registry`: Agent CRUD, owners, cryptographic public keys, lifecycle status (`active`, `suspended`, `revoked`).
- `anubis.services.auth`: Asymmetric challenge-response authentication, key rotation, JWKS endpoint (`/.well-known/jwks.json`), and JWT minting.
- `anubis.services.policy`: Open Policy Agent integration with fallback local evaluation.
- `anubis.services.gateway`: Model Context Protocol (MCP) tool interception and proxying.
- `anubis.services.audit`: Append-only, cryptographic hash-chained transaction log with verify endpoint.
- `anubis.services.approvals`: Human-in-the-loop holding queue for high-risk actions.
