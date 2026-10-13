import os
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from anubis.services.gateway.models import Tool


class CredentialBroker:
    """
    Manages downstream credentials so agents NEVER handle or see raw API keys / secrets.
    The gateway injects credentials on behalf of authorized agents.
    """

    def __init__(self):
        # In-memory vault fallback for static environment secrets
        self._vault: Dict[str, str] = {
            "DB_READ_SECRET": "sec_live_db_readonly_49819284",
            "EMAIL_GATEWAY_TOKEN": "sec_live_smtp_bearer_8831920",
            "FINANCE_CORE_KEY": "sec_live_fin_mtls_99218274",
        }

    def register_secret(self, key_ref: str, secret_value: str):
        self._vault[key_ref] = secret_value

    def get_credential_for_tool(self, db: Session, tool_name: str) -> Optional[str]:
        # Check database for tool-specific credential
        tool = db.query(Tool).filter(Tool.name == tool_name).first()
        if tool and tool.downstream_secret_value:
            return tool.downstream_secret_value
        if tool and tool.downstream_credential_ref:
            return self._vault.get(tool.downstream_credential_ref)

        # Check environment or fallback vault
        env_val = os.getenv(f"SECRET_{tool_name.upper()}")
        if env_val:
            return env_val

        return self._vault.get(f"{tool_name.upper()}_KEY")

    def redact_secrets(self, text_or_dict: Any) -> Any:
        """
        Scans data and redacts any known downstream secrets before returning to agent or logging.
        """
        if isinstance(text_or_dict, str):
            res = text_or_dict
            for secret in self._vault.values():
                if secret and secret in res:
                    res = res.replace(secret, "[REDACTED_SECRET]")
            return res
        elif isinstance(text_or_dict, dict):
            return {k: self.redact_secrets(v) for k, v in text_or_dict.items()}
        elif isinstance(text_or_dict, list):
            return [self.redact_secrets(item) for item in text_or_dict]
        return text_or_dict


credential_broker = CredentialBroker()
