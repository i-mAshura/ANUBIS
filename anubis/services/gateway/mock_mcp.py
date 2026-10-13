from typing import Dict, Any, Optional


class MockMCPServer:
    """
    Simulates downstream MCP servers (e.g. database, email gateway, financial ledger).
    Validates that the ANUBIS Gateway brokered credentials correctly without the agent ever seeing them.
    """

    @staticmethod
    def execute_tool(
        server: str,
        tool_name: str,
        arguments: Dict[str, Any],
        brokered_credential: Optional[str] = None
    ) -> Dict[str, Any]:
        # Tool: read_database / read_data
        if tool_name in ["read_database", "read_data"]:
            return {
                "status": "success",
                "tool": tool_name,
                "server": server,
                "data": [
                    {"id": 1, "record": "Customer Report 2026", "classification": "CONFIDENTIAL"},
                    {"id": 2, "record": "Q3 Analytics", "classification": "INTERNAL"}
                ],
                "authenticated_with_credential_ref": bool(brokered_credential)
            }

        # Tool: send_email
        if tool_name == "send_email":
            recipient = arguments.get("recipient")
            subject = arguments.get("subject", "No Subject")
            return {
                "status": "sent",
                "tool": tool_name,
                "server": server,
                "recipient": recipient,
                "subject": subject,
                "message_id": "msg_98242_anubis"
            }

        # Tool: execute_transfer
        if tool_name == "execute_transfer":
            amount = arguments.get("amount")
            destination = arguments.get("destination")
            return {
                "status": "transferred",
                "tool": tool_name,
                "server": server,
                "amount": amount,
                "destination": destination,
                "tx_hash": "0x4f828a2b5e"
            }

        # Tool: system_shell
        if tool_name == "system_shell":
            command = arguments.get("command")
            return {
                "status": "executed",
                "tool": tool_name,
                "command": command,
                "stdout": "Command completed successfully"
            }

        # Generic / unhandled tool
        return {
            "status": "executed",
            "tool": tool_name,
            "server": server,
            "arguments_processed": len(arguments),
            "authenticated": bool(brokered_credential)
        }
